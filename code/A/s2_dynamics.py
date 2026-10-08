# s2_dynamics.py -- the carry dynamics gamma_{N+1} = (gamma_N + e_N)/(N+1).
# f(a,p) >= K  iff some admissible path survives (gamma_N in Z_p) up to an N with v_p(N!) >= K.
# We track gamma_N modulo p^{K - v_p(N!)} (enough precision: the future constraints up to level K only
# see these digits).  Exact; reproduces known small values as a sanity check of the reformulation.
import sys

def vp(n, p):
    c = 0
    while n % p == 0: n //= p; c += 1
    return c

def ge_K(a, p, K, cap=2_000_000):
    """True iff f(a,p) >= K.  States: gamma_N mod p^{K - v(N!)} ."""
    if K <= 0: return True
    vN = 0  # v_p(a!) computed below
    n = a; v = 0; q = a
    while q: q //= p; v += q
    # time a: gamma_a = 0 (empty sum), e_a = 1 forced
    if v >= K: return True
    M = p ** (K - v)
    states = {0}
    N = a
    first = True
    while True:
        s = vp(N + 1, p)
        newv = v + s
        if newv >= K:
            # S_{N+1} = N!(gamma_N + e_N); need gamma_N + e_N = 0 mod p^{K - v(N!)} = M
            for g in states:
                for e in ((1,) if first else (0, 1)):
                    if (g + e) % M == 0: return True
            return False
        newM = p ** (K - newv)
        inv = pow((N + 1) // p ** s, -1, newM)
        new = set()
        for g in states:
            for e in ((1,) if first else (0, 1)):
                t = (g + e) % M
                if t % (p ** s) == 0:
                    new.add((t // p ** s) * inv % newM)
        first = False
        if not new: return False
        if len(new) > cap: raise RuntimeError("cap")
        states, M, v, N = new, newM, newv, N + 1

def f_exact(a, p, Kmax=400):
    K = 0
    while K < Kmax and ge_K(a, p, K + 1):
        K += 1
    return K

if __name__ == "__main__":
    tests = [(1, 2, 0), (3, 2, 1), (4, 2, 6), (5, 2, 3), (3, 3, 3), (4, 7, 0), (6, 7, 0), (6, 2, 133)]
    for a, p, want in tests:
        got = f_exact(a, p)
        print(f"f({a},{p}) = {got}   (literature/sibling value {want})", "OK" if got == want else "MISMATCH")
        sys.stdout.flush()
    # f(2,2)=254: check f>=254 and not f>=255
    print("f(2,2)>=254:", ge_K(2, 2, 254), " f(2,2)>=255:", ge_K(2, 2, 255))
