# s4_horizon.py -- coverage horizon h(N) = first M > N with Cov(N,M) FALSE, where
#   Cov(N,M): subset sums of {(N+j)!/N! : 0<=j<M-N} cover Z/p^{v_p(M!/N!)}.
# Facts used (proved in the notes): Cov(N,M') => Cov(N,M) for N<M<M'  (monotone), and
#   A_N = Z_p  <=>  Cov(N,M) for all M.  So h(N) finite certifies A_N != Z_p.
# Usage: python3 s4_horizon.py p Nmax maxbits
import sys

def vfact(n, p):
    s = 0
    while n: n //= p; s += n
    return s

def covers(N, M, p):
    K = vfact(M, p) - vfact(N, p)
    Mod = p ** K
    full = (1 << Mod) - 1
    mask, c = 1, 1
    for j in range(M - N):
        if j > 0: c = c * (N + j) % Mod
        x = c
        if x:
            mask |= ((mask << x) | (mask >> (Mod - x))) & full
            if mask == full: return True
    return mask == full

def horizon(N, p, maxbits):
    M = N + 1
    while True:
        K = vfact(M, p) - vfact(N, p)
        if p ** K > 2 ** maxbits: return None, M  # unknown beyond M-1
        if not covers(N, M, p): return M, None
        M += 1

if __name__ == "__main__":
    p, Nmax, maxbits = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    for N in range(1, Nmax + 1):
        h, lim = horizon(N, p, maxbits)
        if h is not None:
            print(f"p={p} N={N}: Cov fails first at M={h}  (v(M!/N!)={vfact(h,p)-vfact(N,p)})")
        else:
            print(f"p={p} N={N}: covers for all M < {lim} (checked to modulus 2^{maxbits})")
        sys.stdout.flush()
