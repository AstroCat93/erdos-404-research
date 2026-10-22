# Independent recomputation of D_p(w,K) from the definition in note_v3 §11.2 (window data).
# Written from scratch by the refute-11.17-counterexample track (round 3).
import sys, math

def v(n, p, cap):
    if n == 0: return cap
    c = 0
    while n % p == 0 and c < cap:
        n //= p; c += 1
    return c

def N_wK(p, w, K, tau):
    P = w * p
    G = min(K, sum(min(v(tau + t, p, K), K) for t in range(1, P + 1)))
    mod = p ** G
    qs = []
    q = 1
    for s in range(P):
        if s > 0: q = q * (tau + s)
        qs.append(q % mod)
    # distinct subset sums mod p^G: bitset DP
    mask = (1 << mod) - 1
    S = 1
    for q in qs:
        # rotate left by q within mod bits
        S = S | (((S << q) | (S >> (mod - q))) & mask) if q else S
    return bin(S).count('1'), G

def D(p, w, K):
    assert w % p != 0
    tot = 0.0
    M = p ** (K - 1)
    cache = {}
    for y in range(M):
        n, G = N_wK(p, w, K, (p * y) % (p ** K))
        tot += math.log(n, p)
    return (p - 1) / (w * p) * tot / M

if __name__ == '__main__':
    for (p, w, K) in [(2,1,2),(2,3,8),(2,3,10),(3,1,4),(3,1,6),(3,1,8),(3,2,6),(5,1,4),(5,1,5),(5,1,7),(5,2,4),(7,1,3),(7,1,5),(2,3,7),(3,2,5),(5,1,4)]:
        print(p, w, K, '%.10f' % D(p, w, K), flush=True)
