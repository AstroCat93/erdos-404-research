# Independent re-implementation (referee). No code shared with note/code.
import itertools, math

def vp(n, p):
    if n == 0: return 10**18
    k = 0
    while n % p == 0:
        n //= p; k += 1
    return k

def vfact(n, p):
    s = 0
    while n:
        n //= p; s += n
    return s

def g_exact(a, p, K, maxstates=None):
    """Exact g_p(a)=max_B v_p(S_B(a)) capped at K (returns K meaning >=K).
    Carry DP on partial sums S_N = sum_{n in T, n<N} n!/a!, with min T = a."""
    if K <= 0: return K
    w = vp(a + 1, p)          # weight of N=a+1: v((a+1)!/a!)
    best = 0
    if w > 0:
        # S = 1 is not divisible by p^w: g = v(1) = 0
        return 0
    states = {1 % p**K}
    N = a + 1
    u = (N // p**vp(N, p)) % p**K  # unit part of N!/a! / p^w  (w = v(N!/a!))
    # invariant: N!/a! = p^w * u, states = {S/p^w mod p^(K-w)}
    while w < K:
        mod = p**(K - w)
        d = vp(N + 1, p)
        newstates = set()
        for s in states:
            for t in (s, (s + u) % mod):
                vt = vp(t, p) if t else K - w
                if vt >= d or w + vt >= K:
                    if w + d >= K:
                        return K
                    newstates.add((t // p**d) % p**(K - w - d))
                else:
                    if w + vt > best: best = w + vt
        if maxstates and len(newstates) > maxstates[0]**maxstates[1]*maxstates[2]:
            # keep a residue-diverse subset: at most `per` states per class mod p^r
            _, r, per = maxstates
            buck = {}
            for s in newstates:
                key = s % p**r
                l = buck.setdefault(key, [])
                if len(l) < per: l.append(s)
            newstates = set(x for l in buck.values() for x in l)
            # NOTE: with sampling, a return of K is still a valid certificate, but
            # a finite return is only a lower bound.
        if not newstates:
            return best
        states = newstates
        w += d
        N += 1
        if w >= K: return K
        u = (u * ((N) // p**vp(N, p))) % p**(K - w)
    return K

def g_brute(a, p, K):
    """brute force over B subset [1, pK) : max v_p(S_B(a)), capped at K"""
    M = p**K
    nb = p*K
    pis = []
    pr = 1
    for b in range(1, nb):
        pr = pr * (a + b) % M
        pis.append(pr)
    best = 0
    # subset sums mod M via set DP of values
    vals = {1 % M}
    for x in pis:
        vals |= {(y + x) % M for y in vals}
    for y in vals:
        v = vp(y, p) if y else K
        best = max(best, min(v, K))
    return best

def gamma(m, p, cap=10**9):
    """gamma_p(m) = max_{B subset [1,m-1]} v_p(1 + sum_b prod_{l=1}^b (l-m)); exact integers"""
    terms = []
    pr = 1
    for b in range(1, m):
        pr *= (b - m)
        terms.append(pr)
    vals = {1}
    for t in terms:
        vals |= {y + t for y in vals}
    best = 0
    for y in vals:
        if y == 0: return float('inf')
        best = max(best, vp(y, p))
    return best

def gamma2(m, p):
    """gamma_p(m) via locality: g_p(p^K - m) with K > log_p(e (m-1)!) bound.
    For small m cross-checked against exact integer enumeration `gamma`."""
    if m == 2: return float('inf')
    bound = math.floor(math.e * math.factorial(m - 1)) if m > 1 else 1
    K = 1
    while p**K <= bound: K += 1
    K += 1
    r = g_exact(p**K - m if p**K > m else p**(K+5) - m, p, K)
    assert r < K
    return r
