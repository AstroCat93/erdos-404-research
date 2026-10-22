"""t1_partition.py -- Lemma B1a (partition, constancy of n_0..n_{l+1} and m_l on A_l(x)),
measurability of B_l (its linear-regime part and eps_l are constant on atoms of G_{l-1}),
for several two-step-predictable adaptive rules, at random x and at x near -k (deep gates).
Also a NEGATIVE CONTROL: a 'one-step' rule (n_{l+1} read from x mod p^{m_l}) breaks the
G_{l-1}-measurability of n_{l+1} (expected to fail; it is outside the hypothesis of B1).
Usage: python3 t1_partition.py SEED NX NLIFT"""
import sys, random
from fz_lib import *

seed, NX, NLIFT = map(int, sys.argv[1:4])
rng = random.Random(seed)
R = 60
stats = dict(lift=0, liftfail=0, Bcheck=0, Bfail=0, epscheck=0, epsfail=0, Bheld=0, deep=0)


def lin_event(X, p, n, l):
    """(D_{l-1}+D_l <= m_{l-1} - M_{n_{l+1}}, M_{n_{l+1}} < m_{l-1}) and its data."""
    vl = vals(X, p, n[l + 1]); V, M = prefix(vl)
    ok = cond52(V, M, n[l - 1], n[l], n[l + 1])
    return ok, (V[n[l]] - V[n[l - 1]], V[n[l + 1]] - V[n[l]], M[n[l + 1]])


def lifts(X, p, m, Tmax):
    """random lifts y of X inside X + p^m Z_p, plus lifts making some y+k deep."""
    out = [X + p ** m * rng.randrange(p ** 30) for _ in range(NLIFT)]
    for k in range(1, Tmax + 1):
        if (X + k) % p ** m == 0:
            for e in (1, 3, 9):
                z = (-(X + k) // p ** m) % p ** e
                out.append(X + p ** m * (z + p ** e * rng.randrange(p ** 10)))
                stats['deep'] += 1
    return out


for p in (3, 5, 7):
    for rule, H in (('lin', p + 3), ('ladder', 2 * p), ('hash', p + 2), ('det', p)):
        for n0 in (2 * p, 2 * p + 3):
            n1 = n0 + 3
            L = 4
            pts = [rng.randrange(p ** R) for _ in range(NX)]
            for k in list(range(1, 12)) + [n0, n0 + 1, n1, n1 + 1, n1 + 2, n1 + 5, n1 + 9]:
                for s in (1, 2, 3, 6, 12):
                    pts.append((-k + p ** s * rng.randrange(1, p ** 30)) % p ** R)
            for X in pts:
                n, m = schedule(X, p, n0, n1, rule, H, L)
                assert all(n[i + 1] > n[i] for i in range(len(n) - 1))
                # refinement A_l(x) subset of A_{l-1}(x)  <=>  m_l >= m_{l-1};  and M_{n_l} < m_l (n_l >= 2p)
                for l in range(1, L + 1):
                    if m[l] < m[l - 1]:
                        stats['liftfail'] += 1; print("FAIL refinement", p, rule, X, m)
                for l in range(0, L + 1):
                    if prefix(vals(X, p, n[l]))[1][n[l]] >= m[l]:
                        stats['liftfail'] += 1; print("FAIL M<V", p, rule, X, n, m)
                for l in range(0, L + 1):
                    for y in lifts(X, p, m[l], n[-1] + 3):
                        ny, my = schedule(y, p, n0, n1, rule, H, l)
                        stats['lift'] += 1
                        if ny[:l + 2] != n[:l + 2] or my[:l + 1] != m[:l + 1]:
                            stats['liftfail'] += 1
                            print("FAIL B1a", p, rule, X, y, l, n, ny, m, my)
                for l in range(1, L + 1):
                    okX, dataX = lin_event(X, p, n, l)
                    if okX:
                        stats['Bheld'] += 1
                        eX = eps_coll(X, p, n[l - 1], n[l], n[l + 1])
                    for y in lifts(X, p, m[l - 1], n[-1] + 3)[:max(3, NLIFT // 2)]:
                        ny, my = schedule(y, p, n0, n1, rule, H, l)
                        assert ny[:l + 2] == n[:l + 2]
                        okY, dataY = lin_event(y, p, ny, l)
                        stats['Bcheck'] += 1
                        if okY != okX or (okX and dataY != dataX):
                            stats['Bfail'] += 1
                            print("FAIL B_l measurability", p, rule, X, y, l, okX, okY, dataX, dataY)
                        if okX:
                            eY = eps_coll(y, p, n[l - 1], n[l], n[l + 1])
                            stats['epscheck'] += 1
                            if eY != eX:
                                stats['epsfail'] += 1
                                print("FAIL eps not constant", p, rule, X, y, l, eX, eY)
        print(f"RESULT p={p} cumulative {stats}")

# NEGATIVE CONTROL: one-step rule n_{l+1} = n_l + 1 + (x mod p^{m_l}) mod H is not a function of
# x mod p^{m_{l-1}}; count atoms of G_{l-1} on which it is not constant.
neg = 0; negt = 0
for p in (3, 5, 7):
    for _ in range(NX):
        X = rng.randrange(p ** R)
        n0 = 2 * p; n1 = n0 + 3
        vl = vals(X, p, n1); V, M = prefix(vl)
        m0 = V[n0]; m1 = V[n1]
        f = lambda Y: n1 + 1 + (Y % p ** m1) % 5
        vals_seen = set(f(X + p ** m0 * rng.randrange(p ** 20)) for _ in range(20))
        negt += 1
        if len(vals_seen) > 1:
            neg += 1
print(f"RESULT negative control (one-step rule): n_2 non-constant on {neg}/{negt} atoms of G_0 (expected > 0 when D_0 > 0)")
print(f"SUMMARY t1 {stats}")
