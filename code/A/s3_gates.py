# s3_gates.py -- (i) p=2: the measure bound mu(A_N) <= 2^{1-s_2(N)} vs finite-horizon covers,
#                      the parity obstruction for Tao blocks [2^j, 2^j');
#               (ii) odd p: coverage of Tao blocks [p^j, p^{j+1}) for small j.
import math

def vfact(n, p):
    s = 0
    while n: n //= p; s += n
    return s

def cover_mask(elems, M):
    """bitmask (python int, bit r set iff r is a subset sum mod M)."""
    full = (1 << M) - 1
    mask = 1
    for x in elems:
        x %= M
        if x == 0: continue
        rot = ((mask << x) | (mask >> (M - x))) & full
        mask |= rot
    return mask

def block_elems(N, H, p, K):
    """(N+j)!/N! mod p^K for 0<=j<H."""
    M = p ** K
    out, c = [], 1
    for j in range(H):
        if j > 0: c = c * (N + j) % M
        out.append(c)
    return out

# (i) p = 2
print("== p=2: finite-horizon upper bound on mu(A_N) vs 2^{1-s2(N)} ==")
worst_ratio = 0
for N in range(1, 25):
    best = 1.0
    for M in range(N + 1, N + 23):
        K = vfact(M, 2) - vfact(N, 2)
        if K > 22: break
        mask = cover_mask(block_elems(N, M - N, 2, K), 2 ** K)
        mu = bin(mask).count("1") / 2 ** K
        best = min(best, mu)
    bound = 2.0 ** (1 - bin(N).count("1"))
    worst_ratio = max(worst_ratio, best / bound)
    print(f"  N={N:2d} s2={bin(N).count('1')}  min_M mu_M(N)={best:.5f}   2^(1-s2)={bound:.5f}")
print("  max ratio (must be <=1):", worst_ratio)

print("== p=2: Tao blocks [2^j,2^j') : #elements L, modulus exponent d, sum of elements mod 2, covers? ==")
for j in range(1, 5):
    for jp in range(j + 1, 6):
        N, H = 2 ** j, 2 ** jp - 2 ** j
        d = vfact(2 ** jp, 2) - vfact(2 ** j, 2)
        T = sum(math.factorial(N + i) // math.factorial(N) for i in range(H))
        cov = None
        if d <= 24:
            cov = bin(cover_mask(block_elems(N, H, 2, d), 2 ** d)).count("1") == 2 ** d
        print(f"  [2^{j},2^{jp}): L={H} d={d} L==d:{H==d} T mod 2={T%2} covers={cov}")

# (ii) odd p Tao blocks
print("== odd p: Tao blocks [p^j, p^{j+1}) coverage of Z/p^d, d = v(p^{j+1}!) - v(p^j!) = p^j ==")
for p, j in [(3, 1), (3, 2), (5, 1), (7, 1), (3, 0), (5, 0), (7, 0)]:
    N, H = p ** j, p ** (j + 1) - p ** j
    d = vfact(p ** (j + 1), p) - vfact(p ** j, p)
    mask = cover_mask(block_elems(N, H, p, d), p ** d)
    c = bin(mask).count("1")
    print(f"  p={p} j={j}: H={H} d={d} covered {c}/{p**d}  ->", "COVERS" if c == p ** d else "fails")
