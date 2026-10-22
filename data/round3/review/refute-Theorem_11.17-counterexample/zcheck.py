# Numerical stress test of the proof of Theorem 11.17 (note_v3 §11.2):
#  - Prop 11.13(a): child zeros alpha_J exist, are simple with slope lambda, v(alpha_J-alpha)=v(Delta_J(alpha))-lambda
#  - formula (11.2): v(z(c)-z(c')) = L_k(z) - lambda + d, d = v(bracket) < G_k
#  - cylinder <=> ball of radius p^{-rho_k}, rho_k constant on cylinders
# Exact p-adic arithmetic with Python ints modulo p^N.
import random, sys, itertools, math

def val(n, p, cap):
    if n == 0: return cap
    c = 0
    while n % p == 0:
        n //= p; c += 1
        if c >= cap: return cap
    return c

def F_and_dF(word_set, x, p, N):
    """word_set: set of j>=1 with e_j=1 (e_0=1 always). Returns F(x), F'(x) mod p^N."""
    mod = p ** N
    top = max(word_set) if word_set else 0
    pi, dpi = 1, 0
    F, dF = 1, 0
    for j in range(1, top + 1):
        dpi = (dpi * (x + j) + pi) % mod
        pi = (pi * (x + j)) % mod
        if j in word_set:
            F = (F + pi) % mod; dF = (dF + dpi) % mod
    return F, dF

def newton(word_set, x, p, N, lam, iters=60):
    mod = p ** N
    for _ in range(iters):
        F, dF = F_and_dF(word_set, x, p, N)
        if F == 0: return x
        if val(dF, p, N) != lam: return None
        vF = val(F, p, N)
        if vF <= 2 * lam: return None
        u = (dF // p ** lam)
        step = (F // p ** lam) * pow(u, -1, mod) % mod
        x = (x - step) % mod
    F, dF = F_and_dF(word_set, x, p, N)
    return x

def find_simple_zeros(p, N, rng, tries=400, maxj=10, m0=6):
    out = []
    for _ in range(tries):
        B = set(j for j in range(1, maxj + 1) if rng.random() < 0.4)
        if not B: continue
        x0 = rng.randrange(p ** m0)
        F, dF = F_and_dF(B, x0, p, N)
        lam = val(dF, p, N)
        if lam >= m0 // 2: continue
        if val(F, p, N) <= 2 * lam: continue
        a = newton(B, x0, p, N, lam)
        if a is None: continue
        F, dF = F_and_dF(B, a, p, N)
        if val(F, p, N) < N - 3 * lam - 5: continue
        if val(a + 2, p, N) > 10: continue  # avoid -2 neighbourhood
        out.append((B, a, lam))
    return out

def run(p, w, K, nwin, N, seed, ncodes):
    rng = random.Random(seed)
    P = w * p
    zs = find_simple_zeros(p, N, rng)
    report = dict(cases=0, pairs=0, fail_1113=0, fail_112=0, fail_cyl=0, fail_rhoconst=0, skipped_prec=0)
    seen = set()
    for (B, a, lam) in zs:
        key = (tuple(sorted(B)), a % p ** 20)
        if key in seen: continue
        seen.add(key)
        if len(seen) > 6: break
        # runs of alpha
        l0 = next(l for l in range(1, p + 1) if (a + l) % p == 0)
        def Lpos(x, n):  # v(pi_n(x))
            return sum(val(x + t, p, N) for t in range(1, n + 1))
        i0 = 0
        while True:
            li = l0 + p * i0
            P0 = Lpos(a, li) - lam
            if li >= p * (2 * lam + 2) and li > max(B) and P0 >= max(K + 1, val(a + 2, p, N) + 1):
                break
            i0 += 1
        ak = [l0 + p * (i0 + k * w) for k in range(nwin + 1)]
        prec = N - 4 * lam - 8
        # codes: random subsets per window
        codes = [tuple(frozenset(s for s in range(P) if rng.random() < 0.5) for k in range(nwin)) for _ in range(ncodes)]
        # force some pairs that first differ in each window
        base = codes[0]
        for k in range(nwin):
            for _ in range(3):
                c = list(base); c[k] = frozenset(s for s in range(P) if rng.random() < 0.5)
                for m in range(k + 1, nwin): c[m] = frozenset(s for s in range(P) if rng.random() < 0.5)
                codes.append(tuple(c))
        zc = {}
        for c in codes:
            J = set(ak[k] + s for k in range(nwin) for s in c[k])
            W = set(B) | J
            z = newton(W, a, p, N, lam)
            if z is None:
                report['fail_1113'] += 1; print('NEWTON FAIL', p, B, c); continue
            F, dF = F_and_dF(W, z, p, N)
            if val(dF, p, N) != lam: report['fail_1113'] += 1; print('slope changed', p, B, c)
            # Delta_J(alpha)
            Fa, _ = F_and_dF(W, a, p, N)
            pred = val(Fa, p, N) - lam
            got = val(z - a, p, N)
            if min(pred, got) < prec and pred != got:
                report['fail_1113'] += 1; print('11.13 dist mismatch', pred, got)
            zc[c] = z
        report['cases'] += 1
        cl = list(zc.keys())
        for c1, c2 in itertools.combinations(cl, 2):
            if c1 == c2: continue
            k = next(k for k in range(nwin) if c1[k] != c2[k])
            z, z2 = zc[c1], zc[c2]
            Lk = Lpos(z, ak[k])
            # bracket at z
            br = 0; q = 1
            for s in range(P):
                if s > 0: q *= (z + ak[k] + s)
                if s in c1[k]: br += q
                if s in c2[k]: br -= q
            d = val(br % p ** N, p, N)
            gk = sum(val(z + ak[k] + t, p, N) for t in range(1, P + 1))
            tau = (a + ak[k]) % p ** K
            Gk = min(K, sum(min(val(tau + t, p, K), K) for t in range(1, P + 1)))
            vd = val(z - z2, p, N)
            if Lk + d - lam >= prec or vd >= prec:
                report['skipped_prec'] += 1; continue
            report['pairs'] += 1
            if d < gk:
                if vd != Lk - lam + d:
                    report['fail_112'] += 1; print('(11.2) FAIL', p, w, K, B, k, vd, Lk, lam, d, gk)
            if d < Gk:
                rho = Lk + Gk - lam
                # cylinder <=> ball checks for all depths
                for kk in range(nwin):
                    rho_kk = Lpos(z, ak[kk]) + min(K, sum(min(val(((a + ak[kk]) % p**K) + t, p, K), K) for t in range(1, P + 1))) - lam
                    rho_kk2 = Lpos(z2, ak[kk]) + min(K, sum(min(val(((a + ak[kk]) % p**K) + t, p, K), K) for t in range(1, P + 1))) - lam
                    agree = all(c1[m] == c2[m] for m in range(kk + 1))
                    if agree != (vd >= rho_kk):
                        report['fail_cyl'] += 1; print('cyl FAIL', kk, agree, vd, rho_kk)
                    if agree and rho_kk != rho_kk2:
                        report['fail_rhoconst'] += 1; print('rho const FAIL')
    return report

if __name__ == '__main__':
    for (p, w, K, nwin, N) in [(2, 1, 2, 3, 160), (2, 3, 4, 3, 200), (3, 1, 3, 3, 120), (3, 2, 3, 3, 140), (5, 1, 2, 3, 100), (7, 1, 2, 2, 90)]:
        for seed in range(3):
            r = run(p, w, K, nwin, N, seed, 10)
            print(p, w, K, 'seed', seed, r, flush=True)
