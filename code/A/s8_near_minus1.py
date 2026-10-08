# s8_near_minus1.py -- exact values of g(a,p)=f(a,p)-v_p(a!) on the classes a = -1-t (mod p^k), p^k > M_t, t>=2:
#   g(a,p) = max_{sigma in Sigma_t} v_p(sigma),  Sigma_t = { sum_{j in J} (-1)^j t!/(t-j)! : 0 in J subset [0,t] }.
# Verified here against the independent carry-dynamics oracle ge_K (s2_dynamics) on explicit a.
from math import factorial
from s2_dynamics import ge_K

def vp(n, p):
    n = abs(n); c = 0
    while n % p == 0: n //= p; c += 1
    return c

def vfact(n, p):
    s = 0
    while n: n //= p; s += n
    return s

def Sigma(t):
    S = {1}
    for j in range(1, t + 1):
        x = (-1) ** j * factorial(t) // factorial(t - j)
        S |= {s + x for s in S}
    return S

ok = True
for p in [2, 3, 5, 7]:
    for t in range(2, 8):
        S = Sigma(t); Mt = max(abs(s) for s in S)
        assert 0 not in S
        k = 1
        while p ** k <= Mt: k += 1
        g = max(vp(s, p) for s in S)
        # verify on a = -1-t + p^k*w for w=1,2 (natural numbers, a>=1)
        for w in (1, 2, 3):
            a = -1 - t + p ** k * w
            if a < 1: continue
            K0 = vfact(a, p)
            good = ge_K(a, p, K0 + g) and not ge_K(a, p, K0 + g + 1)
            if not good: ok = False
            print(f"p={p} t={t} M_t={Mt} k={k}: a={a}: predicted g={g}; oracle agrees: {good}")
print("ALL OK" if ok else "MISMATCH")
