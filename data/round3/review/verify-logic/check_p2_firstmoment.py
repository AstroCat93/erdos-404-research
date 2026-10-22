# Numerical sanity check of Prop 11.26 (Hensel first-moment bound) and of the slope certificates
# (Prop 11.25) at p=2: integrate Z_n = 2^{V_n-n}|P_n| over C ∩ Gamma_* exactly mod 2^Q, and record max slope.
import numpy as np, sys, itertools
Q = int(sys.argv[1]) if len(sys.argv) > 1 else 22
MOD = 1 << Q
def v2arr(a):
    a = a.copy(); out = np.zeros(a.shape, dtype=np.int64)
    z = (a == 0); a[z] = 1
    while True:
        m = (a & 1) == 0
        if not m.any(): break
        out[m] += 1; a[m] >>= 1
    out[z] = 99
    return out
for name, r0, k, L, Vcert, n in [("C0", 0, 3, 1, 4, 10), ("C2", 2, 3, 3, 7, 12), ("C6", 6, 4, 6, 11, 14)]:
    x = (np.arange(MOD >> k, dtype=np.int64) << k) + r0
    pis = [np.ones_like(x)]; dpis = [np.zeros_like(x)]
    vals = []
    for j in range(1, n + 1):
        vals.append(v2arr((x + j) % MOD))
        pis.append(pis[-1] * ((x + j) % MOD) % MOD)
        dpis.append((dpis[-1] * ((x + j) % MOD) + pis[-2]) % MOD)
    V = np.sum(vals, axis=0); Mx = np.max(vals, axis=0)
    good = (Mx < Q - 2) & (V >= max(Vcert, 2 * L + 1, L + k)) & (V - L > Mx) & (V < Q - 8)
    cnt = np.zeros_like(x); maxslope = 0
    for bits in itertools.product((0, 1), repeat=n - 1):
        e = (1,) + bits
        S = np.zeros_like(x); dS = np.zeros_like(x)
        for j in range(n):
            if e[j]: S = (S + pis[j]) % MOD; dS = (dS + dpis[j]) % MOD
        alive = good & ((S & ((np.int64(1) << V) - 1)) == 0)
        if alive.any():
            sl = v2arr(dS[alive]); maxslope = max(maxslope, int(sl.max()))
        cnt += alive
    Z = cnt.astype(float) * np.exp2(V - n)
    integral = Z[good].sum() / float(MOD)
    bound = 2.0 ** (L - 1 + max(0, L + 1 - k))
    print(f"{name}: n={n} Q={Q} integral over C∩Gamma_* of Z_n = {integral:.5f} (bound {bound}); E[Z_n|C∩Gamma]~{Z[good].mean():.3f}; max slope of alive paths {maxslope} (cert <= {L}); excluded mass {1 - good.mean():.3e} of C")
