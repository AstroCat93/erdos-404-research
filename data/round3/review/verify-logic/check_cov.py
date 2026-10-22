# Referee check (verify-logic, round 3): Theorem 11.45 bounds and its "Consequence",
# Theorem 11.46(b) fibre criterion vs direct covering, Remark 11.49 Cov(13,3,H), H=19..32.
import math, random
from fractions import Fraction

def v(z, p):
    z = Fraction(z)
    if z == 0: return 10**9
    a, b = z.numerator, z.denominator; k = 0
    while a % p == 0: a //= p; k += 1
    while b % p == 0: b //= p; k -= 1
    return k

def vfact(u, p):
    s = 0; q = p
    while q <= u: s += u // q; q *= p
    return s

def covered_count(elems, M):
    mask = (1 << M) - 1; S = 1
    for q in elems:
        q %= M
        if q: S |= ((S << q) | (S >> (M - q))) & mask
    return bin(S).count('1')

def ys(p, t, H, K, M):
    X = p ** t * K; out = []; y = 1
    for i in range(H):
        if i > 0: y = y * (X - (H - i)) % M
        out.append(y)
    return out

print("== Theorem 11.45: bounds (a),(b),(d) and the 'Consequence' ==")
random.seed(1)
for p, D, t in [(3, 2, 3), (3, 3, 4), (5, 2, 3), (2, 3, 4), (3, 2, 5), (7, 2, 3)]:
    H = p ** D; c = vfact(H - 1, p); Mtop = t + c
    worst = 0; viol = 0; reach = []
    for trial in range(30):
        K = random.randrange(1, 10**6)
        X = p ** t * K
        y = Fraction(1); A = Fraction(1); B = Fraction(1)
        for i in range(H):
            if i > 0:
                s = i
                y *= (X - (H - s)); A *= (1 - Fraction(p ** D, s)); B *= (1 + Fraction(X, s - p ** D))
            l = 0 if i == 0 else int(math.floor(math.log(i, p) + 1e-12))
            assert y == math.factorial(i) * A * B
            if i > 0:
                assert v(A - 1, p) >= D - l and v(B - 1, p) >= t + v(K, p) - l, (p, D, t, i)
            dv = v(y - math.factorial(i) * A, p)
            assert dv >= t + v(K, p) + vfact(i, p) - l
            if dv >= Mtop: reach.append((i, dv))
            dv2 = v(y - math.factorial(i), p)
            if dv2 >= Mtop: reach.append(("i!", i, dv2))
    print(f" p={p} D={D} t={t} H={H} c={c} top={Mtop}: bounds hold; elements with y_i == i!A_i (or i!) mod p^(t+c): {sorted(set(reach), key=str)[:12]}{' ...' if len(set(reach)) > 12 else ''}")

print("== Theorem 11.46(b): fibre criterion == direct covering, miss counts add up ==")
def Vp(p):
    e = [(-1) ** u * math.factorial(p - 1) // math.factorial(u) for u in range(p)]
    s = {0}
    for x in e: s = s | {z + x for z in s}
    return sorted(s)
for p, t, Hp, npos in [(3, 2, 3, 99), (3, 3, 3, 99), (3, 3, 5, 60), (5, 2, 5, 60), (5, 3, 4, 40), (7, 2, 3, 40)]:
    H = p * Hp; c = vfact(H - 1, p); Mx = t + c; Mod = p ** Mx
    V = Vp(p); agree = 0; ncov = 0
    units = [K for K in range(1, p ** c) if K % p] if c > 0 else [1]
    random.seed(2); poss = units if len(units) <= npos else random.sample(units, npos)
    for K in poss:
        el = ys(p, t, H, K, Mod)
        direct_miss = Mod - covered_count(el, Mod)
        # fibre form
        R = {0}
        for q in el[:p * (Hp - 1)]:
            R = R | {(r + q) % Mod for r in R}
        ylast = el[p * (Hp - 1)]
        assert v(ylast, p) == c
        u = (ylast // p ** c) % p ** t
        fib_miss = 0
        for T in range(p ** c):
            BT = {((r - T) // p ** c) % p ** t for r in R if (r - T) % p ** c == 0}
            sums = {(b + u * w) % p ** t for b in BT for w in V}
            fib_miss += p ** t - len(sums)
        assert fib_miss == direct_miss, (p, t, Hp, K, fib_miss, direct_miss)
        agree += 1; ncov += (direct_miss == 0)
    print(f" p={p} t={t} H={H} c={c}: {agree} positions, fibre miss total == direct miss count on all; covered at {ncov}")

print("== Remark 11.49: Cov(13,3,H) for H=19..32 ==")
p, t = 13, 3
res = {}
for H in range(19, 33):
    c = vfact(H - 1, p); Mod = p ** (t + c)
    ok = True
    for K in range(1, p ** c):
        if K % p == 0: continue
        if covered_count(ys(p, t, H, K, Mod), Mod) < Mod: ok = False; break
    res[H] = ok
print(" ", res)
