#!/usr/bin/env python3
"""Adversarial random tests of the key inequalities of R3Q (data/round3/reports/R3Q.md), written
independently of code/round3/R3Q.  Exact integer arithmetic modulo 2^P (P = 600) only; a 2-adic x is a random
integer mod 2^P (every quantity used below is determined far below 2^P).

Own helpers: pi_j(x+eps) mod (eps^3, 2^P) carried as triples (Taylor coefficients 0,1,2); alive paths found by
breadth-first extension (a prefix of an alive word is alive); rho_n^{(lam)} from the note's definition with
exactly 2*lam terms (convolution over Z/2^lam), not the 'stop when v(c_i) >= lam' variant of the track.

usage: lemma_tests.py SEED  (runs all tests, prints counts and failures)"""
import sys, random, time
from fractions import Fraction as Fr

P = 600
MOD = 1 << P

def v(a):
    a %= MOD
    if a == 0: return P
    return (a & -a).bit_length() - 1

def s2(n): return bin(n).count("1")
def flog2(n): return n.bit_length() - 1
def beta(n): return n - s2(n) - flog2(n)
def z(n): return (n + 1) // 2 - 1

def pis(x, N):
    """list of (pi_j, pi_j^{[1]}, pi_j^{[2]}) at x, j = 0..N, mod 2^P (triples = Taylor coefficients)."""
    out = [(1, 0, 0)]
    a0, a1, a2 = 1, 0, 0
    for j in range(1, N + 1):
        c = x + j          # multiply by (c + eps)
        a0, a1, a2 = (a0 * c) % MOD, (a1 * c + a0) % MOD, (a2 * c + a1) % MOD
        out.append((a0, a1, a2))
    return out

def Vlist(x, N):
    V = [0]
    for j in range(1, N + 1): V.append(V[-1] + v(x + j))
    return V

def alive(x, N, PI=None, V=None, cap=60000):
    """dict: length-N word (tuple) -> (S, S', S^[2]) mod 2^P for all words alive at N."""
    if PI is None: PI = pis(x, N)
    if V is None: V = Vlist(x, N)
    cur = {(1,): (1, 0, 0)}
    for L in range(1, N):
        nxt = {}
        p = PI[L]
        for e, (a, b, c) in cur.items():
            for bit in (0, 1):
                t = ((a + p[0]) % MOD, (b + p[1]) % MOD, (c + p[2]) % MOD) if bit else (a, b, c)
                if v(t[0]) >= V[L + 1]:
                    nxt[e + (bit,)] = t
        cur = nxt
        if len(cur) > cap: return None
    return cur

def slope(t): return v(t[1])

def pi_n(x, n):
    p = 1
    for i in range(1, n + 1): p = p * (x + i) % MOD
    return p

def target(x, n, S, prec=200):
    """tau_n = -S / pi_n(x) mod 2^prec (requires v(S) >= v(pi_n))."""
    p = pi_n(x, n); m = v(p)
    assert v(S) >= m
    return ((-S) % MOD >> m) * pow((p >> m) % (1 << prec), -1, 1 << prec) % (1 << prec)

def rho_table(x, n, lam):
    """rho_n^{(lam)}(s), s mod 2^lam, as Fractions: 2^lam * P(sum_{i<2lam} g_i pi_{n+i}/pi_n == s)."""
    if lam == 0: return [Fr(1)]
    m = 1 << lam
    dist = [0] * m; dist[0] = 1
    c = 1
    for i in range(2 * lam):
        if i > 0: c = c * (x + n + i) % m
        nd = dist[:]
        for t in range(m):
            if dist[t]: nd[(t + c) % m] += dist[t]
        dist = nd
    tot = 1 << (2 * lam)
    return [Fr(d * m, tot) for d in dist]

def rand_even(rng):
    """random even 2-adic x; mixture of uniform, near -2, and with a planted large valuation."""
    r = rng.random()
    x = rng.getrandbits(P) & ~1
    if r < 0.25:          # near -2: v(x+2) = j
        j = rng.randint(2, 9)
        u = rng.getrandbits(P - j - 1) | 1
        x = (-2 + (u << j)) % MOD
    elif r < 0.4:         # planted large valuation v(x+i) >= b at some small even i
        i = 2 * rng.randint(1, 20); b = rng.randint(6, 14)
        x = (-i + (rng.getrandbits(P - b) << b)) % MOD
    return x % MOD

# ----------------------------------------------------------------------------------------------- tests
def test_L1(rng, cnt, fails, reps):
    for _ in range(reps):
        x = rand_even(rng)
        if x % 2: continue
        N = 220
        vs = [None] + [v(x + i) for i in range(1, N + 1)]
        V = Vlist(x, N)
        for n in range(1, N + 1):
            M = max(vs[1:n + 1])
            cnt["L1c"] += 1
            if V[n] - M < beta(n): fails.append(("L1c", x, n))
            if n >= 2 and V[n] > n + M - 2: fails.append(("L1b", x, n))
            # Lemma 2(c): if M_T <= G - T + 2 and T >= 2 then V_T <= G; take G = T + M - 2 (smallest allowed)
            if n >= 2 and V[n] > n + M - 2: fails.append(("L2c", x, n))
        for _ in range(40):
            n = rng.randint(0, 150); i = rng.randint(0, 60)
            cnt["L1a"] += 1
            if V[n + i] - V[n] < max(i - s2(i), i // 2): fails.append(("L1a", x, n, i))
        # walk drop (e): W_{n0+N_K} - W_{n0} <= 1 - s(r), N_K <= 2^K
        for _ in range(20):
            n0 = rng.randint(0, 100); K = rng.randint(1, 9)
            zz = x + n0
            NK = next(Nn for Nn in range(1, (1 << K) + 1) if (zz + Nn) % (1 << K) == 0)
            r = zz % (1 << K)
            V2 = Vlist(x, n0 + NK)
            W = lambda t: t - V2[t]
            cnt["L1e"] += 1
            if W(n0 + NK) - W(n0) > 1 - s2(r): fails.append(("L1e", x, n0, K))
        # truncated Lemma 1(b): sum_{i<=L} min(v(y+i),c) <= L + mu - 2 (L>=2, mu>=1)
        for _ in range(20):
            y = rng.getrandbits(P); L = rng.randint(2, 40); c = rng.randint(1, 8)
            tv = [min(v(y + i), c) for i in range(1, L + 1)]
            mu = max(tv)
            cnt["L1b_trunc"] += 1
            if mu >= 1 and sum(tv) > L + mu - 2: fails.append(("L1b_trunc", y, L, c))

def test_L3_L4(rng, cnt, fails, reps):
    classes = [(0, 8, 1, 6), (2, 16, 3, 8), (6, 16, 3, 10)]
    for _ in range(reps):
        cls = rng.randrange(6)
        x = rng.getrandbits(P)
        if cls < 3:
            r, m, lam, nC = classes[cls]
        elif cls == 3: r, m = 10, 16
        elif cls == 4: r, m = 4, 8
        else: r, m = rng.choice([(14, 16), (2, 4), (0, 2)])
        x = (x - x % m + r) % MOD
        N = rng.randint(4, 44)
        PI = pis(x, N); V = Vlist(x, N)
        al = alive(x, N, PI, V)
        if al is None: cnt["L4_skipped"] += 1; continue
        cnt["L4"] += 1
        if len(al) > 2 ** z(N): fails.append(("L4", x, N, len(al)))
        if cls < 3 and N >= nC:
            for e, t in al.items():
                cnt["L3_slope"] += 1
                if slope(t) != lam: fails.append(("L3", cls, x, N, e))
        if cls == 3 and N >= 6 and al: fails.append(("L3d", x, N))
        if cls == 4 and N >= 4 and al: fails.append(("L3e", x, N))
        if cls == 3 and N >= 6: cnt["L3d"] += 1
        if cls == 4 and N >= 4: cnt["L3e"] += 1

def test_L5(rng, cnt, fails, budget_s):
    """one-step identity, everything recomputed from scratch at x' = x + 2^m w for all w mod 2^{D+lam+1}."""
    t0 = time.time()
    while time.time() - t0 < budget_s:
        x = rand_even(rng)
        if x % 2: continue
        n = rng.randint(6, 30)
        PI = pis(x, n + 1); V = Vlist(x, n + 1)
        al = alive(x, n, PI, V)
        if not al: continue
        m = V[n]; M = max(v(x + i) for i in range(1, n + 1)); D = v(x + n + 1)
        for e, t in al.items():
            lam = slope(t)
            if lam > 7 or not (lam + D <= m - M and lam < m - M):
                cnt["L5_skip_hyp"] += 1; continue
            if D + lam > 9: cnt["L5_skip_big"] += 1; continue
            tau0 = target(x, n, t[0])
            rho_n = rho_table(x, n, lam)[tau0 % (1 << lam)] if lam else Fr(1)
            rhs = Fr(2) ** (1 - D) * rho_n
            nw = 1 << (D + lam + 1)
            tot = Fr(0); tot1 = 0
            ok = True
            for w in range(nw):
                xp = (x + (w << m)) % MOD
                PIp = pis(xp, n + 1)
                Vp = Vlist(xp, n + 1)
                # S_e at x' from scratch
                S = [0, 0, 0]
                for j, bit in enumerate(e):
                    if bit:
                        for q in range(3): S[q] = (S[q] + PIp[j][q]) % MOD
                if v(S[0]) < Vp[n] or v(S[1]) != lam: ok = False; break      # parent must stay alive, same slope
                rt = rho_table(xp, n + 1, lam)
                for f in (0, 1):
                    S0 = (S[0] + f * PIp[n][0]) % MOD; S1 = (S[1] + f * PIp[n][1]) % MOD
                    if v(S0) >= Vp[n + 1]:
                        if v(S1) != lam: ok = False
                        tc = target(xp, n + 1, S0)
                        tot += rt[tc % (1 << lam)] if lam else Fr(1)
                        tot1 += 1
            cnt["L5"] += 1
            if lam >= 3: cnt["L5_lam>=3"] += 1
            if not ok: fails.append(("L5_slope", x, n, e)); continue
            lhs = tot / nw
            if lhs != rhs: fails.append(("L5", x, n, e, lhs, rhs))
            # negative control: the same identity with rho := 1 (E #children = 2^{1-D}) is false in general
            if Fr(tot1, nw) != Fr(2) ** (1 - D): cnt["L5_control_rho1_differs"] += 1

def test_L6(rng, cnt, fails, reps):
    for _ in range(reps):
        x = rand_even(rng)
        if x % 2: continue
        n = rng.randint(1, 120); lam = rng.randint(1, 11)
        tab = rho_table(x, n, lam)
        Mt = max(min(v(x + n + i), lam) for i in range(1, 2 * lam + 1))
        ub = Fr(2) ** min(lam - 1, (lam + Mt) // 2 - 1)
        cnt["L6b"] += 1
        if max(tab) > ub: fails.append(("L6b", x, n, lam, max(tab), ub))
        if sum(tab) != (1 << lam): fails.append(("L6a_mean", x, n, lam))
        if max(tab) == ub: cnt["L6b_attained"] += 1
    # lower bound (c): alive e with slope lam and an alive extension at n + 2 lam
    for _ in range(reps // 3):
        x = rand_even(rng)
        if x % 2: continue
        n = rng.randint(6, 24)
        NN = n + 2 * 12
        PI = pis(x, NN); V = Vlist(x, NN)
        al_n = alive(x, n, PI, V)
        if not al_n: continue
        for e, t in al_n.items():
            lam = slope(t)
            if lam < 1 or lam > 12: continue
            alN = alive(x, n + 2 * lam, PI, V)
            if alN is None: continue
            if not any(w[:n] == e for w in alN): continue
            rho = rho_table(x, n, lam)[target(x, n, t[0]) % (1 << lam)]
            cnt["L6c"] += 1
            if rho < Fr(1, 2 ** flog2(2 * lam)): fails.append(("L6c", x, n, e, rho))

def test_L8(rng, cnt, fails, reps):
    for _ in range(reps):
        j = rng.randint(2, 7)
        u = rng.getrandbits(P - j - 1) | 1
        x = (-2 + (u << j)) % MOD
        assert v(x + 2) == j
        N = rng.randint(3 * j + 2, 3 * j + 22)
        PI = pis(x, N); V = Vlist(x, N)
        for n in range(4, N + 1):
            if V[n] < 3 * j + 1: continue
            al = alive(x, n, PI, V)
            if al is None: break
            for e, t in al.items():
                cnt["L8"] += 1
                if v(t[1]) > 2 * j:
                    cnt["L8_hi_slope"] += 1
                    if v(t[2]) > j: fails.append(("L8", x, n, e))
            break

def test_L9(rng, cnt, fails, budget_s):
    """Lemma 9 (a),(b),(d) with general thresholds; U_N(x') recomputed from scratch for all relevant w."""
    t0 = time.time()
    while time.time() - t0 < budget_s:
        j = rng.choice([2, 2, 2, 3, 3, 4])
        u = rng.getrandbits(P - j - 1) | 1
        x = (-2 + (u << j)) % MOD
        n = rng.randint(7, 28); L = rng.randint(1, 6); N = n + L
        PI = pis(x, N); V = Vlist(x, N)
        vs = [None] + [v(x + i) for i in range(1, N + 1)]
        m = V[n]; Mn = max(vs[1:n + 1]); MN = max(vs[1:N + 1]); D = V[N] - m; mp = m - Mn
        Tn = max(Mn, 2 * j + 1, D + Mn)
        if Tn > mp: continue
        if not (MN < mp and D <= mp - MN and m >= 3 * j + 1 and m - 2 * MN > j): continue
        if rng.random() < 0.5:
            TN = rng.randint(Tn, min(2 * mp, Tn + 10))
        else:                      # thresholds where the decay factor 2^{-(TN - m' - 1 - j)} is active
            lo, hi = max(Tn, mp + j + 2), min(2 * mp, mp + j + 7)
            if lo > hi: continue
            TN = rng.randint(lo, hi)
        E = max(TN, V[N]) - mp
        if E > 11: continue
        al = alive(x, n, PI, V)
        if al is None: continue
        Un = {e for e, t in al.items() if slope(t) >= Tn}
        cnt["L9_windows"] += 1
        if not Un: continue
        cnt["L9_nonempty"] += 1
        nw = 1 << (max(E, 0) + 1)
        tot = 0; okab = True
        al_N = alive(x, N, PI, V)
        for e2, t2 in al_N.items():          # Lemma 8 consequence used in (d): v(S_c^[2](x)) = kappa <= j
            if e2[:n] in Un:
                cnt["L9_kappa"] += 1
                if v(t2[2]) > j: fails.append(("L9_kappa", x, n, N, e2))
        for w in range(nw):
            xp = (x + (w << mp)) % MOD
            PIp = pis(xp, N); Vp = Vlist(xp, N)
            alp_n = alive(xp, n, PIp, Vp)
            Unp = {e for e, t in alp_n.items() if slope(t) >= Tn}
            if Unp != Un: okab = False
            alp_N = alive(xp, N, PIp, Vp)
            UN = [e for e, t in alp_N.items() if slope(t) >= TN]
            if set(e2 for e2 in alp_N if e2[:n] in Un) != set(e2 for e2 in al_N if e2[:n] in Un): okab = False  # (c)
            for e2, t2 in alp_N.items():     # Taylor congruence of (d): S'_c(x') = S'_c(x) + 2^{m'+1} w S_c^[2](x) mod 2^{2m'}
                if e2[:n] in Un and e2 in al_N:
                    cnt["L9_taylor"] += 1
                    if (t2[1] - al_N[e2][1] - (w << (mp + 1)) * al_N[e2][2]) % (1 << (2 * mp)) != 0:
                        fails.append(("L9_taylor", x, n, N, e2, w))
            for e2 in UN:
                if e2[:n] not in Un: okab = False
            tot += len(UN)
        avg = Fr(tot, nw)
        bound = len(Un) * Fr(2) ** (L - (L - 1) // 2 - max(0, TN - mp - 1 - j))
        if not okab: fails.append(("L9ab", x, n, N, Tn, TN))
        if avg > bound: fails.append(("L9d", x, n, N, Tn, TN, avg, bound))
        r = avg / bound
        if r > cnt.get("L9_max_ratio_x1000", 0) / 1000: cnt["L9_max_ratio_x1000"] = int(r * 1000)
        if TN - mp - 1 - j > 0 and avg > 0: cnt["L9_nonempty_with_decay"] += 1

if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    rng = random.Random(seed)
    from collections import Counter
    cnt, fails = Counter(), []
    T = {}
    for name, fn, arg in (("L1", test_L1, 300), ("L3L4", test_L3_L4, 3000), ("L6", test_L6, 3000),
                          ("L8", test_L8, 1500), ("L5", test_L5, 420), ("L9", test_L9, 420)):
        t0 = time.time(); fn(rng, cnt, fails, arg); T[name] = round(time.time() - t0, 1)
        print(f"[{name}] done in {T[name]} s; counts so far: {dict(cnt)}; failures so far: {len(fails)}", flush=True)
    for f in fails[:20]: print("FAIL", f)
    print("TOTAL failures:", len(fails))
