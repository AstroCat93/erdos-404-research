# s1_structure.py -- numerical checks of the exact p-adic structure lemmas (A-structure).
# All checks are exact integer arithmetic.  Usage: python3 s1_structure.py
import math, sys

def vp(n, p):
    if n == 0: return 10**9
    c = 0
    while n % p == 0: n //= p; c += 1
    return c

def vfact(n, p):  # Legendre
    s, q = 0, n
    while q: q //= p; s += q
    return s

def P(n, p):  # product of 1<=j<=n with p !| j
    r = 1
    for j in range(1, n + 1):
        if j % p: r *= j
    return r

def U(n, p):
    return math.factorial(n) // p ** vfact(n, p)

def gamma_p_int(m, p):  # Morita Gamma_p(m) for integer m>=1: (-1)^m prod_{j<m, p!|j} j
    return (-1) ** m * P(m - 1, p)

ok = True
# T1: U(n) = U(n//p) * P(n) ;  P(n) = (-1)^{n+1} Gamma_p(n+1);  U(n) = prod_i P(n//p^i)
for p in [2, 3, 5, 7]:
    for n in range(0, 400):
        if U(n, p) != U(n // p, p) * P(n, p): ok = False; print("T1a fail", p, n)
        if P(n, p) != (-1) ** (n + 1) * gamma_p_int(n + 1, p): ok = False; print("T1b fail", p, n)
        prod, q = 1, n
        while q: prod *= P(q, p); q //= p
        if prod != U(n, p): ok = False; print("T1c fail", p, n)
print("T1 (recursion, Morita form, product formula):", ok)

# T2: P(n+p^k) = eps * P(n) mod p^k, eps=-1 (p odd or p^k in {2,4}), +1 (p=2,k>=3); minimal period of P mod p^k
def Pmod_seq(p, k, length):
    M = p ** k; out = []; r = 1
    out.append(1)
    for n in range(1, length):
        if n % p: r = r * n % M
        out.append(r)
    return out

def min_period(seq, maxT):
    for T in range(1, maxT + 1):
        if all(seq[i] == seq[i + T] for i in range(len(seq) - T)):
            return T
    return None

t2 = True
for p in [2, 3, 5, 7]:
    for k in range(1, 6 if p < 5 else 4):
        M = p ** k
        seq = Pmod_seq(p, k, 6 * M + 10)
        eps = 1 if (p == 2 and k >= 3) else -1
        if p == 2 and k == 1: eps = 1  # mod 2 everything is 1 == -1
        for n in range(0, 4 * M):
            if (seq[n + M] - eps * seq[n]) % M: t2 = False; print("T2 fail", p, k, n)
        T = min_period(seq, 3 * M)
        pred = 2 * M if p != 2 else (1 if k == 1 else (8 if k == 2 else M))
        print(f"  P mod {p}^{k}: minimal period {T} (predicted {pred})")
        if T != pred: t2 = False
print("T2 (antiperiodicity, exact minimal periods):", t2)

# T3: closed formula for U(n) mod p^k (p odd):
#   U(n) = (-1)^{v_p(floor(n/p^{k-1})!)} * prod_{i>=0} P(floor(n/p^i) mod p^k)  (mod p^k)
# p=2,k>=3: U(n) = prod_i P(floor(n/2^i) mod 2^k) (mod 2^k)
t3 = True
for p in [2, 3, 5, 7]:
    for k in ([3, 4, 5] if p == 2 else [1, 2, 3]):
        M = p ** k
        Ptab = Pmod_seq(p, k, M)
        for n in range(0, 3000):
            prod, q = 1, n
            while q: prod = prod * Ptab[q % M] % M; q //= p
            if p != 2:
                prod = prod * (-1) ** vfact(n // p ** (k - 1), p) % M
            if prod % M != U(n, p) % M: t3 = False; print("T3 fail", p, k, n); break
print("T3 (closed digit formula for U mod p^k):", t3)

# T3': U mod p^k is NOT a function of finitely many low digits: U(p^j) = (-1)^j mod p (p odd)
t3b = all(U(p ** j, p) % p == (-1) ** j % p for p in [3, 5, 7] for j in range(0, 6))
print("T3' U(p^j) == (-1)^j mod p for p=3,5,7, j<=5:", t3b)

# T4: block multiplicativity: U(p^k q + r) = U(q) * Phi_k(q mod 2p^{k-1}, r) mod p^k (p odd),
#     with q mod 2^{k-1} for p=2, k>=3.  Report minimal period in q of q -> U(p^k q + r)/U(q) mod p^k.
t4 = True
for p in [2, 3, 5]:
    for k in ([3, 4] if p == 2 else [1, 2, 3]):
        M = p ** k
        per_pred = (2 * p ** (k - 1)) if p != 2 else 2 ** (k - 1)
        worst = 0
        for r in range(0, M):
            seq = []
            for q in range(0, 4 * per_pred + 8):
                uq = U(q, p) % M
                seq.append(U(M * q + r, p) * pow(uq, -1, M) % M)
            T = min_period(seq, 2 * per_pred + 2)
            if T is None or per_pred % T: t4 = False; print("T4 fail", p, k, r, T)
            worst = max(worst, T or 0)
        print(f"  p={p},k={k}: max over r of minimal q-period = {worst} (bound {per_pred})")
print("T4 (block multiplicativity):", t4)

# T5: grouping identity n=pm+r: n! = p^m m! P(pm) h_r(m), h_r(m)=prod_{j=1}^r (pm+j); P(pm) = (-1)^m mod p
t5 = True
for p in [2, 3, 5, 7]:
    for m in range(0, 40):
        W = P(p * m, p)
        if (W - (-1) ** m) % p: t5 = False
        for r in range(p):
            h = 1
            for j in range(1, r + 1): h *= p * m + j
            if math.factorial(p * m + r) != p ** m * math.factorial(m) * W * h: t5 = False; print("T5 fail", p, m, r)
print("T5 (grouping identity with W_m=P(pm)=(-1)^m mod p):", t5)
