# Brute-force check of weight conservation (Theorem A mechanism) WITHOUT using the lemmas:
# pick (path p of length N0, point y) valid & 1-stable at N0, ball U = y + 2^sigma Z_2.
# Enumerate classes of U mod 2^(sigma+K); for a random representative of each class enumerate ALL valid
# continuations of p up to time n = N0+T; sum  2^-K * 2^{P_n(y')-n}  and compare with 2^{P_N0(y)-N0}.
import random, sys
BIG = 600
MOD = 1 << BIG
def v2(n):
    n %= MOD
    if n == 0: return BIG
    return (n & -n).bit_length() - 1
def gamma_mod(y, path):
    # returns (gamma_n mod 2^{BIG-P}, P) or None if invalid
    g = 0; prec = BIG; P = 0
    for k, e in enumerate(path):
        n = k + 1; d = v2(y + n); t = (g + e) % (1 << prec)
        if d and (t & ((1 << d) - 1)): return None
        prec -= d; P += d
        u = ((y + n) >> d) % (1 << prec)
        g = ((t >> d) * pow(u, -1, 1 << prec)) % (1 << prec)
    return g, P
def kappa(y, path):
    # B_n(y,y) = sum gamma_i pi_{i-1} mod 2^200
    K2 = 1 << 200; B = 0; pi = 1; g = 0; prec = BIG
    for k, e in enumerate(path):
        n = k + 1; d = v2(y + n); t = (g + e) % (1 << prec)
        prec -= d; u = ((y + n) >> d) % (1 << prec)
        g = ((t >> d) * pow(u, -1, 1 << prec)) % (1 << prec)
        B = (B + g * pi) % K2; pi = (pi * (y + n)) % K2
    return v2(B) if B else 200
def continuations(y, path, n):
    out = []
    stack = [tuple(path)]
    while stack:
        q = stack.pop()
        if gamma_mod(y, q) is None: continue
        if len(q) == n: out.append(q); continue
        stack.append(q + (0,)); stack.append(q + (1,))
    return out
rnd = random.Random(int(sys.argv[1])); trials = int(sys.argv[2])
done = 0; exact = 0; worst = 0.0
while done < trials:
    N0 = rnd.randrange(8, 20); T = rnd.randrange(2, 7)
    y = rnd.getrandbits(BIG) & ~1
    paths = continuations(y, (1,), N0)
    if not paths: continue
    p = rnd.choice(paths)
    gm = gamma_mod(y, p); P = gm[1]
    kap = kappa(y, p); M = max(v2(y + l) for l in range(1, N0 + 1))
    sig = P - kap
    if not (sig >= kap + M + 1): continue
    n = N0 + T
    Pn_y = P + sum(v2(y + l) for l in range(N0 + 1, n + 1))
    K = Pn_y - P + 1
    if K > 13: continue
    total = 0.0
    for j in range(1 << K):
        yj = (y + (j << sig) + (rnd.getrandbits(BIG) << (sig + K))) % MOD
        for q in continuations(yj, p, n):
            Pn = sum(v2(yj + l) for l in range(1, n + 1))
            total += 2.0 ** (Pn - n - K)
    target = 2.0 ** (P - N0)
    rel = total / target
    done += 1; exact += abs(rel - 1) < 1e-12; worst = max(worst, abs(rel - 1))
    print(f"N0={N0} T={T} kappa={kap} sigma={sig} M={M} K={K}  descendant/initial weight = {rel:.6f}")
print("trials", done, "exactly conserved", exact, "max deviation", worst)
