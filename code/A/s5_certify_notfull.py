# s5_certify_notfull.py -- computer-assisted proof that A_N != Z_p for all N in explicit residue classes.
#
# A_N := { sum_{n>=N} e_n n!/N! : e in {0,1}^N }  (compact subset of Z_p).
# Facts (proved in the write-up):
#   (F1) A_N = Z_p  iff  Cov(N,M) for every M>N, where Cov(N,M): the subset sums of
#        pi_j(N) := prod_{l=1}^{j} (N+l), 0<=j<M-N, cover Z/p^{K}, K = v_p(M!/N!).
#   (F2) Cov(N,M) implies the same subset sums cover Z/p^{K'} for every K'<=K.
#   (F3) pi_j(N) mod p^{K'} depends only on N mod p^{K'} (products of congruent integers).
# Certificate for a class N = r (mod p^t): some s0<=t and K'<=t with
#   L := distance from N to the next multiple of p^{s0} (determined by r),
#   K' <= K0 := s0 + sum_{1<=l<L} v_p(r+l)  (a lower bound for v_p((N+L)!/N!) on the whole class),
#   and the subset sums of {pi_j(r) mod p^{K'} : j < L} do NOT cover Z/p^{K'}.
# Then Cov(N, N+L) fails for every N in the class, hence A_N != Z_p.
# Classes not certified at level t are split into p classes at level t+1.
# Usage: python3 s5_certify_notfull.py p T
import sys

def vp(n, p):
    if n == 0: return 99
    c = 0
    while n % p == 0: n //= p; c += 1
    return c

def covers_mod(r, L, p, K):
    Mod = p ** K
    full = (1 << Mod) - 1
    mask, c = 1, 1
    for j in range(L):
        if j > 0: c = c * (r + j) % Mod
        if c:
            mask |= ((mask << c) | (mask >> (Mod - c))) & full
            if mask == full: return True
    return mask == full

def certify(r, t, p):
    """return (s0, L, K') certificate or None"""
    for s0 in range(1, t + 1):
        q = p ** s0
        L = (-r) % q
        if L == 0: L = q
        K0 = s0 + sum(vp(r + l, p) for l in range(1, L))
        for Kp in range(1, min(K0, t) + 1):
            if not covers_mod(r % p ** Kp, L, p, Kp):
                return (s0, L, Kp)
    return None

if __name__ == "__main__":
    p, T = int(sys.argv[1]), int(sys.argv[2])
    alive = [0]  # classes mod p^0
    for t in range(1, T + 1):
        cand = [r + i * p ** (t - 1) for r in alive for i in range(p)]
        alive, certs = [], {}
        for r in cand:
            c = certify(r, t, p)
            if c is None: alive.append(r)
            else: certs[r] = c
        dens = len(alive) / p ** t
        print(f"p={p} t={t}: {len(cand)} classes tested, {len(alive)} not excluded "
              f"(density {dens:.6f})")
        if len(alive) <= 40: print("   surviving classes mod p^t:", sorted(alive))
        sys.stdout.flush()
