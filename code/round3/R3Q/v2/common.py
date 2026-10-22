"""Shared exact helpers for the R3Q (restarted) lemma tests. x is an integer standing for a 2-adic
number known mod 2^P (P large); every quantity used is determined far below 2^P."""
P = 640
MOD = 1 << P
def v2(a):
    a %= MOD
    return (a & -a).bit_length() - 1 if a else P
def s2(n): return bin(n).count("1")
def beta(n): return n - s2(n) - (n.bit_length() - 1)
def env(x, n):
    """V_n, M_n"""
    vs = [v2(x + i) for i in range(1, n + 1)]
    return sum(vs), max(vs) if vs else 0
def taylor_pis(x, N):
    """pi_j^{[i]}(x) mod 2^P for i=0,1,2 and j=0..N."""
    p0, p1, p2 = [1], [0], [0]
    for j in range(1, N + 1):
        a = x + j
        p2.append((p2[-1] * a + p1[-1]) % MOD)
        p1.append((p1[-1] * a + p0[-1]) % MOD)
        p0.append((p0[-1] * a) % MOD)
    return p0, p1, p2
def alive_paths(x, n, cap=200000):
    """All words e (tuple of bits, e_0=1) of length n with v(S_e(x)) >= V_n(x), by BFS over prefixes
    (backward integrality: a prefix of an alive word is alive). Returns list of (e, S, S', S2)."""
    p0, p1, p2 = taylor_pis(x, n)
    V = [0]
    for j in range(1, n + 1): V.append(V[-1] + v2(x + j))
    pop = [((1,), 1, 0, 0)]
    for L in range(1, n):          # extend words of length L to L+1, keep those alive at L+1
        new = []
        for e, S, S1, S2 in pop:
            for b in (0, 1):
                if b: T = ((S + p0[L]) % MOD, (S1 + p1[L]) % MOD, (S2 + p2[L]) % MOD)
                else: T = (S, S1, S2)
                if v2(T[0]) >= V[L + 1]:
                    new.append((e + (b,),) + T)
        pop = new
        if len(pop) > cap: return None
    return [q for q in pop if v2(q[1]) >= V[n]]
def rho(x, n, lam, s):
    """rho_n^{(lam)}(s) = 2^lam P(sum_i g_i pi_{n+i}(x)/pi_n(x) == s mod 2^lam), exact (Fraction)."""
    from fractions import Fraction
    if lam == 0: return Fraction(1)
    m = 1 << lam
    dist = {0: 1}; tot = 1; c = 1; i = 0
    while v2(c) < lam:
        cm = c % m; nd = {}
        for t, k in dist.items():
            nd[t] = nd.get(t, 0) + k
            u = (t + cm) % m; nd[u] = nd.get(u, 0) + k
        dist = nd; tot *= 2; i += 1; c *= (x + n + i)
    return Fraction(dist.get(s % m, 0) * m, tot)
def target(x, n, S):
    """tau_n = -S/pi_n(x) as an integer mod 2^(P - V_n - 8) (S divisible by 2^{V_n})."""
    p = 1
    for i in range(1, n + 1): p = p * (x + i) % MOD
    V = v2(p); prec = P - V - 8
    return ((-S % MOD) >> V) * pow(p >> V, -1, 1 << prec) % (1 << prec)
