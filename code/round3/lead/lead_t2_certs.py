# Lead-author independent check of the finite cases behind T2 Proposition 2.3
# (round 3, note section 11).  Shares no code with T2's certs.py.
# Route: instead of evaluating the renormalised Phi_e(y) at y=-m, evaluate the
# integer S_e(x) = sum_j e_j pi_j(x) at x = -m-2 and use S_e = y(y-1) Phi_e(y),
# y = x+2, which gives v2(Phi_e(-m)) = v2(S_e(-m-2)) - v2(m) - v2(m+1).
# Also re-checks the identity S_e = y(y-1)Phi_e(y) at random 2-adic-like integers.
import random
from itertools import product
from fractions import Fraction

def v2(n):
    n = Fraction(n)
    if n == 0:
        return None
    a, b, v = abs(n.numerator), n.denominator, 0
    while a % 2 == 0:
        a //= 2; v += 1
    while b % 2 == 0:
        b //= 2; v -= 1
    return v

def pi(j, x):
    r = 1
    for i in range(1, j + 1):
        r *= (x + i)
    return r

def S(word, x):
    return sum(pi(j, x) for j, e in enumerate(word) if e)

out = []
# (a): x = -4, words e0=1, (e1,e2,e3) free; pi_j(-4)=0 for j>=4
vals = [S((1, e1, e2, e3), -4) for e1, e2, e3 in product((0, 1), repeat=3)]
assert all(v != 0 for v in vals)
out.append("(a) S_e(-4) over 8 words: %s ; max v2 = %d" % (vals, max(v2(v) for v in vals)))

def phi_vals(m, e2, e3, nfree):
    # words with e0=e1=1, e2, e3 fixed, e_4..e_{3+nfree} free; S_e(-m-2) has pi_j=0 for j>=m+2
    res = []
    for t in product((0, 1), repeat=nfree):
        w = (1, 1, e2, e3) + t
        s = S(w, -m - 2)
        ph = Fraction(s, (-m) * (-m - 1))      # y(y-1) at y=-m
        res.append(ph)
    return res

for (m, e2, e3, nfree, label) in [(4, 1, 0, 2, "Phi(-4), e2=1,e3=0 (cases b,c)"),
                                   (4, 0, 1, 2, "Phi(-4), e2=0,e3=1 (case b)"),
                                   (8, 0, 1, 6, "Phi(-8), e2=0,e3=1 (case c)")]:
    ph = phi_vals(m, e2, e3, nfree)
    assert all(q != 0 for q in ph)
    vs = [v2(q) for q in ph]
    hist = {v: vs.count(v) for v in sorted(set(vs))}
    out.append("%s: %d cases, values %s, max v2 = %d, histogram %s" %
               (label, len(ph), sorted(set(ph)) if len(ph) <= 4 else "(64 values)", max(vs), hist))

# identity S_e(x) = y(y-1) Phi_e(y), Phi_e(y) = e2 - 1/(1-y) + sum_{k>=1} e_{k+2} pi_k(y), for words with e1=1
random.seed(20261021)
bad = 0
for trial in range(2000):
    n = random.randint(3, 14)
    w = [1, 1] + [random.randint(0, 1) for _ in range(n - 2)]
    x = random.randint(-10**6, 10**6)
    y = x + 2
    if y in (0, 1):
        continue
    phi = Fraction(w[2]) - Fraction(1, 1 - y) + sum(w[k + 2] * pi(k, y) for k in range(1, n - 2))
    if Fraction(S(w, x)) != y * (y - 1) * phi:
        bad += 1
out.append("identity S_e = y(y-1)Phi_e(y): 2000 random (word, x), failures = %d" % bad)
# Proposition 6.2(a): S_{1,3}(x) = (x+2)^3
out.append("S_{1,3}(x) - (x+2)^3 at x=-50..50: all zero = %s" %
           all(S((1, 1, 0, 1), x) == (x + 2) ** 3 for x in range(-50, 51)))
print("\n".join(out))
