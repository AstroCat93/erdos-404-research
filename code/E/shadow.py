"""gamma(m,p) := g(-m,p) for the p-adic integer -m  (m >= 1).
   P_T(-m) = (-1)^(m-1) * C(I),  C(I) = sum_{i in I} (-1)^i (m-1)!/i!,  I = {m-1-k : k in T} contains m-1.
   gamma(m,p) = max_I v_p(C(I))  (infinite iff some C(I) = 0, which happens only for m = 2).
   Exact enumeration of all 2^(m-1) values C(I) (no modulus)."""
import sys, math

def all_C(m):
    j = m - 1
    vals = [1 if j % 2 == 0 else -1]          # i = j term, forced
    for i in range(j):
        t = (-1) ** i * (math.factorial(j) // math.factorial(i))
        vals = vals + [v + t for v in vals]
    return vals

def vp(x, p):
    v = 0
    while x % p == 0:
        x //= p; v += 1
    return v

def gamma_all(m, primes):
    vals = all_C(m)
    out = {}
    if any(v == 0 for v in vals):
        return {p: math.inf for p in primes}
    for p in primes:
        out[p] = max(vp(v, p) for v in vals)
    return out

if __name__ == '__main__':
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    print("# gamma(m,p) = g(-m,p);  f(a,p) = v_p(a!) + gamma(m,p) for all a == -m mod p^(gamma+1)")
    print("# m  " + " ".join(f"{p:>4}" for p in primes) + "   floor(log_2(e*(m-1)!))")
    for m in range(1, M + 1):
        g = gamma_all(m, primes)
        print(f"{m:4d} " + " ".join(f"{('inf' if g[p] == math.inf else g[p]):>4}" for p in primes)
              + f"   {int(math.log2(math.e * math.factorial(m - 1)))}")
        sys.stdout.flush()
