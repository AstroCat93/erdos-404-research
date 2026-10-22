# Thm 11.45 'Consequence' with unit positions K' (as in Cov): does any y_i agree with i!A_i, or with i!,
# modulo p^(t+c) (the full demand) for the family H = p^(t-1)?
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
random.seed(7)
for p, t in [(3, 3), (3, 4), (5, 3), (2, 4), (2, 5), (7, 3), (3, 5)]:
    D = t - 1; H = p ** D; c = vfact(H - 1, p); top = t + c
    hitsA = set(); hitsF = set(); maxgapA = -99; maxgapF = -99
    for trial in range(60):
        K = random.randrange(1, 10**6)
        if K % p == 0: K += 1
        X = p ** t * K; y = 1; A = Fraction(1)
        for i in range(H):
            if i > 0: y *= (X - (H - i)); A *= (1 - Fraction(p ** D, i))
            dA = v(y - math.factorial(i) * A, p); dF = v(y - math.factorial(i), p)
            if i > 0:
                maxgapA = max(maxgapA, dA - top); maxgapF = max(maxgapF, dF - top)
                if dA >= top: hitsA.add(i)
                if dF >= top: hitsF.add(i)
    print(f"p={p} t={t} H={H} c={c} demand p^{top}: i with y_i==i!A_i mod demand: {sorted(hitsA)}; with y_i==i! mod demand: {sorted(hitsF)}; max(v-demand) A:{maxgapA} F:{maxgapF}")
