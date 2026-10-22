# hensel_check.py -- numerical sanity checks (exact arithmetic mod p^N) for
# Proposition 2.1, Lemma 2.2 and the distance formula (3.1) of Theorem 3.1.
# Not part of any proof.  Usage: python3 hensel_check.py
import random, itertools, math
random.seed(20261021)

def v(a, p, N):
    a %= p**N
    if a == 0: return N
    c = 0
    while a % p == 0: a //= p; c += 1
    return c

def FdF(word, x, p, N):
    """F_e(x), F_e'(x) mod p^N for a finite set 'word' of positions (0 included)."""
    M = p**N; F = 0; dF = 0; pi = 1; dpi = 0
    top = max(word)
    for j in range(top + 1):
        if j > 0:
            dpi = (dpi * (x + j) + pi) % M
            pi = (pi * (x + j)) % M
        if j in word:
            F = (F + pi) % M; dF = (dF + dpi) % M
    return F, dF

def newton(word, x0, p, N, lam):
    M = p**N; x = x0 % M
    for _ in range(4 * N):
        F, dF = FdF(word, x, p, N)
        if F == 0: break
        assert v(dF, p, N) == lam
        u = (dF // p**lam) % M
        t = F // p**lam
        x = (x - t * pow(u, -1, M)) % M
    return x

def simple_zero(p, r, N):
    """Theorem 3.5 construction: a finite T with a simple zero in class r."""
    kst = next(k for k in range(1, p + 1) if (r + k) % p == 0)
    for size in range(0, kst + 1):
        for T in itertools.combinations(range(1, kst + 1), size):
            word = {0, *T}
            F, dF = FdF(word, r, p, 1)
            if F % p == 0 and dF % p != 0:
                a = newton(word, r, p, N, 0)
                if (a + 2) % p**N == 0: continue   # alpha=-2 excluded (Theorem 3.1)
                return word, a
    return None

def check_prop21(p, N=60):
    out = []
    for r in range(p):
        sz = simple_zero(p, r, N)
        if sz is None: out.append((r, 'none(frozen or only -2)')); continue
        word, a = sz
        F, dF = FdF(word, a, p, N); lam = v(dF, p, N)
        n0 = p * (2 * lam + 2) + max(word) + 1
        ok = 0
        for j in range(n0, n0 + 3 * p):
            w2 = set(word) | {j}
            b = newton(w2, a, p, N, lam)
            Fb, dFb = FdF(w2, b, p, N)
            pij = math.prod(a + t for t in range(1, j + 1))
            pred = v(pij, p, N) - lam
            if Fb % p**(N - 2 * lam - 2) == 0 and v(dFb, p, N) == lam and v(b - a, p, N) == pred:
                ok += 1
        out.append((r, sorted(word), lam, ok, 3 * p))
    return out

def check_lemma22(p, c, N=60, seed=False):
    word = {0, 1, 2, c + 2}
    # direct: H(y)=y+(y-1)pi_c(y), Hensel from y=0
    M = p**N; y = 0
    for _ in range(4 * N):
        pc = math.prod(y + t for t in range(1, c + 1)) % M
        H = (y + (y - 1) * pc) % M
        if H == 0: break
        dpc = sum(math.prod(y + t for t in range(1, c + 1) if t != i) for i in range(1, c + 1)) % M
        dH = (1 + pc + (y - 1) * dpc) % M
        y = (y - H * pow(dH, -1, M)) % M
    xc = (y - 2) % M
    F, dF = FdF(word, xc, p, N)
    if seed: return word, xc, v(dF, p, N)
    return (F == 0, v(y, p, N), v(math.factorial(c), p, N), v(dF, p, N))

def check_distance(p, w=1, ncodes=12, N=80):
    sz = next((simple_zero(p, r, N) for r in range(p) if simple_zero(p, r, 5) is not None), None)
    if sz is None:
        word, a, lam = check_lemma22(p, 2 * p, N, seed=True)
    else:
        word, a = sz
        F, dF = FdF(word, a, p, N); lam = v(dF, p, N)
    l0 = next(l for l in range(1, p + 1) if (a + l) % p == 0)
    i0 = (p * (2 * lam + 2) + max(word)) // p + 2
    P = w * p; nwin = 3
    starts = [l0 + p * (i0 + k * w) for k in range(nwin)]
    codes = []
    for _ in range(ncodes):
        codes.append([frozenset(s for s in range(P) if random.random() < 0.5) for k in range(nwin)])
    zs = []
    for c in codes:
        J = set(word)
        for k in range(nwin): J |= {starts[k] + s for s in c[k]}
        zs.append(newton(J, a, p, N, lam))
    bad = 0; tested = 0; nontriv = 0
    for i, j in itertools.combinations(range(ncodes), 2):
        c, cp = codes[i], codes[j]
        k = next((k for k in range(nwin) if c[k] != cp[k]), None)
        if k is None: continue
        z = zs[i]
        Lk = v(math.prod(z + t for t in range(1, starts[k] + 1)), p, N)
        q = lambda s: math.prod(z + starts[k] + t for t in range(1, s + 1))
        d = v(sum(q(s) for s in c[k]) - sum(q(s) for s in cp[k]), p, N)
        Lk1 = v(math.prod(z + t for t in range(1, starts[k] + P + 1)), p, N)
        pred = Lk - lam + d if d < Lk1 - Lk else None
        got = v(zs[i] - zs[j], p, N)
        tested += 1
        if pred is not None:
            nontriv += 1
            if got != pred: bad += 1
    return dict(p=p, lam=lam, pairs=tested, checked=nontriv, failures=bad)

if __name__ == '__main__':
    for p in (2, 3, 5, 7):
        print('Prop2.1', p, check_prop21(p))
    for p in (2, 3, 5, 7):
        print('Lemma2.2', p, check_lemma22(p, 2 * p), check_lemma22(p, 3 * p + 1))
    for p in (2, 3, 5, 7):
        print('dist(3.1)', check_distance(p, w=1), check_distance(p, w=2))
