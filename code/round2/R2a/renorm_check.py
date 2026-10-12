"""Numerical check of the renormalisation identity (exact identity, checked in floating point):

  T_{N0}(k) = sum_{w' unit mod p^(k-W)} |nu_{N_W}^(w'/p^(k-W))| * H_W( (w' * abar mod p^(k-W)) / p^k )

where x'_n = n!/N0!, N_W = first n with v(n!) - v(N0!) >= W, A = N_W!/N0! = p^W * a,
abar = a^{-1} mod p^(k-W), G(theta) = prod_{N0<=n<N_W} |cos(pi theta x'_n)|,
H_W(theta) = sum_{s mod p^W} G(theta + s/p^W)   (period p^-W),
and nu_{N_W}^ uses x''_n = n!/N_W! for n >= N_W.
Also prints sup/mean of H_W on a fine grid (sup >= H_W(0) >= 1: prefix-sup bounds cannot decay).
usage: python3 renorm_check.py p N0 W k
"""
import sys, math

def v(n, p):
    c = 0
    while n % p == 0:
        n //= p; c += 1
    return c

def main():
    p, N0, W, k = map(int, sys.argv[1:5])
    vN0 = sum(v(i, p) for i in range(1, N0 + 1))
    # element list n >= N0 with relative level < k
    ns = []
    n = N0; lv = 0
    while lv < k:
        ns.append((n, lv)); n += 1; lv += v(n, p)
    NW = next(n for (n, l) in ns if l >= W)
    xp = {}
    f = 1
    for (n, l) in ns:
        if n > N0: f *= n
        xp[n] = f            # n!/N0!
    M = p ** k
    # direct shell sum
    T = 0.0
    for u in range(1, M):
        if u % p == 0: continue
        pr = 1.0
        for (n, l) in ns:
            pr *= abs(math.cos(math.pi * ((u * xp[n]) % M) / M))
        T += pr
    # renormalised form
    A = xp[NW]; assert A % p ** W == 0 and (A // p ** W) % p != 0
    a = A // p ** W
    q = p ** (k - W)
    abar = pow(a, -1, q)
    bot = [xp[n] for (n, l) in ns if l < W]
    top = [xp[n] // A for (n, l) in ns if l >= W]   # n!/N_W!
    def G(r, D):   # G(r/D), exact residues
        res = 1.0
        for x in bot: res *= abs(math.cos(math.pi * ((r * x) % D) / D))
        return res
    def H(r, D):   # H(r/D) with p^W | D
        return sum(G(r + s * (D // p ** W), D) for s in range(p ** W))
    T2 = 0.0
    for w in range(1, q):
        if w % p == 0: continue
        pr = 1.0
        for x in top: pr *= abs(math.cos(math.pi * ((w * x) % q) / q))
        T2 += pr * H((w * abar) % q, M)
    print(f"p={p} N0={N0} W={W} k={k}  direct T={T:.10e}  renormalised={T2:.10e}  rel.diff={abs(T-T2)/T:.2e}")
    D = p ** (W + 6)
    hv = [H(i, D) for i in range(0, D // p ** W, max(1, D // p ** W // 20000))]
    print(f"H_W: H(0)={H(0, D):.6f}  max(grid)={max(hv):.6f}  mean(grid)={sum(hv)/len(hv):.6e}  min(grid)={min(hv):.3e}")
    print(f"p^W * prod-mean heuristic (p(2/pi)^p)^W ~ {(p*(2/math.pi)**p)**W:.4e}")

main()
