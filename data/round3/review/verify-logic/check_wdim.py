# Referee check: independent implementation of D_p(w,K) (definition before Thm 11.17).
# usage: python3 check_wdim.py p w K
import sys, math

def v(z, p, cap):
    if z == 0: return cap
    k = 0
    while z % p == 0 and k < cap: z //= p; k += 1
    return k

def ndistinct(qs, M):
    mask = (1 << M) - 1
    S = 1
    for q in qs:
        q %= M
        if q: S |= ((S << q) | (S >> (M - q))) & mask
    return bin(S).count('1')

def D(p, w, K):
    P = w * p; mod = p ** K
    cache = {}; tot = 0.0
    for y in range(p ** (K - 1)):
        tau = p * y
        G = min(K, sum(min(v((tau + t) % mod, p, K), K) for t in range(1, P + 1)))
        M = p ** G; key = (G, tau % M)
        if key not in cache:
            qs = []; q = 1
            for s in range(P):
                if s > 0: q = q * (tau + s) % M
                qs.append(q)
            cache[key] = ndistinct(qs, M)
        tot += math.log(cache[key], p)
    return (p - 1) / (w * p) * tot / p ** (K - 1)

if __name__ == "__main__":
    p, w, K = map(int, sys.argv[1:4])
    print(p, w, K, "%.10f" % D(p, w, K))
