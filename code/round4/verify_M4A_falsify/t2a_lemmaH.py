"""t2a: exact test of M4A Lemma H (Hensel step) on random and adversarial polynomials.
For S in Z[X], a ball B = x0 + p^b Z_p, 1 <= k <= k', theta = min(ceil(k/2), k-b+1),
 H = {z in B: v(S(z)) >= k, v(S'(z)) >= theta}:
   p^k' mu_B{v(S)>=k'} - p^k mu_B{v(S)>=k}  ==  p^k' mu_B(H & {v(S)>=k'}) - p^k mu_B(H).
Exact: enumerate x mod p^max(k',b) in B.  Control: theta+1 in place of theta (should fail sometimes).
usage: python3 t2a_lemmaH.py p SEED NTEST
"""
import sys, random
from fractions import Fraction

p = int(sys.argv[1]); seed = int(sys.argv[2]); NT = int(sys.argv[3])
random.seed(seed)


def poly_eval(cf, x, mod):
    r = 0
    for a in reversed(cf):
        r = (r * x + a) % mod
    return r


def deriv(cf):
    return [i * cf[i] for i in range(1, len(cf))]


def mul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] += x * y
    return r


def vmodp(a, mod):
    if a % mod == 0:
        return 10 ** 6
    v = 0
    while a % p == 0:
        a //= p; v += 1
    return v


def random_poly():
    kind = random.choice(("rand", "sq", "cube", "near", "signed"))
    if kind == "rand":
        return [random.randint(-p ** 3, p ** 3) for _ in range(random.randint(2, 8))], kind
    if kind == "signed":   # a signed carry polynomial sum d_c pi_c(X + shift)
        t = random.randint(2, 3 * p)
        sh = random.randint(-2 * p, 2 * p)
        cf = [0]
        pi = [1]
        for c in range(t):
            d = 1 if c == 0 else random.choice((-1, 0, 0, 1))
            m = max(len(cf), len(pi))
            cf = [(cf[i] if i < len(cf) else 0) + d * (pi[i] if i < len(pi) else 0) for i in range(m)]
            pi = mul(pi, [sh + c + 1, 1])
        return cf, kind
    z = random.randint(-p ** 4, p ** 4)
    base = [random.randint(-p, p) or 1 for _ in range(random.randint(1, 3))]
    if kind == "sq":
        return mul(mul([-z, 1], [-z, 1]), base), kind
    if kind == "cube":
        return mul(mul(mul([-z, 1], [-z, 1]), [-z, 1]), base), kind
    # near double root: (X-z)^2 + p^j c
    j = random.randint(1, 6)
    q = mul([-z, 1], [-z, 1])
    q[0] += p ** j * random.choice((1, -1, 2))
    return mul(q, base), kind


ok = bad = ctrl_fail = trivial = 0
kinds = {}
for _ in range(NT):
    S, kind = random_poly()
    if all(a == 0 for a in S):
        continue
    Sd = deriv(S)
    b = random.randint(0, 4)
    k = random.randint(1, 6 if p == 3 else 4)
    kp = random.randint(k, k + (3 if p == 3 else 2))
    x0 = random.randrange(p ** max(b, 1)) if b > 0 else 0
    # bias: half the time put x0 near a root of S mod p^b
    if b > 0 and random.random() < 0.5:
        roots = [z for z in range(p ** b) if poly_eval(S, z, p ** b) == 0]
        if roots:
            x0 = random.choice(roots)
    theta = min(-(-k // 2), k - b + 1)
    R = max(kp, b)
    mod = p ** R
    pts = [(x0 + p ** b * j) % mod for j in range(p ** (R - b))]
    N = len(pts)

    def measures(th):
        a_k = a_kp = h = h_kp = 0
        for z in pts:
            vs = vmodp(poly_eval(S, z, mod), mod)
            vd = vmodp(poly_eval(Sd, z, mod), mod) if Sd else 10 ** 6
            if vs >= k:
                a_k += 1
                if vd >= th:
                    h += 1
                    if vs >= kp:
                        h_kp += 1
            if vs >= kp:
                a_kp += 1
        lhs = Fraction(p ** kp * a_kp - p ** k * a_k, N)
        rhs = Fraction(p ** kp * h_kp - p ** k * h, N)
        return lhs, rhs

    lhs, rhs = measures(theta)
    if theta <= 0:
        trivial += 1
    if lhs == rhs:
        ok += 1
    else:
        bad += 1
        print("FAIL", kind, S, x0, b, k, kp, theta, lhs, rhs)
    kinds[kind] = kinds.get(kind, 0) + 1
    if theta >= 1:
        l2, r2 = measures(theta + 1)
        if l2 != r2:
            ctrl_fail += 1
print(f"p={p}: Lemma H identity: {ok} exact equalities, {bad} failures (of which theta<=0 trivial: {trivial}); kinds {kinds}")
print(f"control (theta+1 in place of theta): identity fails in {ctrl_fail} cases")
