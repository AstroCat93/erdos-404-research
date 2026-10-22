"""m4c_lib.py -- exact p-adic helpers for track M4C (round 4).  Written for this track; the conventions are
those of note.md section 10.1 / R3M section 1:
  pi_j(x) = (x+1)...(x+j), V_n = v(pi_n(x)), M_n = max_{i<=n} v(x+i), c_n = 2^-n p^{V_n};
  a path of length n is (e_0..e_{n-1}) with e_0 = 1, S_e = sum e_j pi_j; alive at n iff v(S_e(x)) >= V_n;
  target tau_n = -S_e/pi_n; slope = v(S_e'(x)).
All arithmetic is with Python integers modulo p^PREC (exact as long as every valuation used is < PREC).
"""
from fractions import Fraction


def v(a, p, cap):
    """p-adic valuation of the integer a, capped at cap (a read modulo p^cap)."""
    a %= p ** cap
    if a == 0:
        return cap
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k


def products(x, N, p, prec):
    """pi[j], dpi[j] = pi_j(x), pi_j'(x) mod p^prec for j=0..N, and vals[i] = v(x+i) (i=1..N; vals[0]=0)."""
    mod = p ** prec
    pi = [1] * (N + 1)
    dpi = [0] * (N + 1)
    vals = [0] * (N + 1)
    for j in range(1, N + 1):
        pi[j] = pi[j - 1] * (x + j) % mod
        dpi[j] = (dpi[j - 1] * (x + j) + pi[j - 1]) % mod
        vals[j] = v(x + j, p, prec)
    return pi, dpi, vals


def cumV(vals):
    out = [0] * len(vals)
    for j in range(1, len(vals)):
        out[j] = out[j - 1] + vals[j]
    return out


def alive_paths(pi, dpi, Vc, n0, n1, roots, p, prec):
    """All extensions to length n1 (alive at n1) of the paths in roots (each (S, dS, bits) alive at n0).
    Depth-first with prefix pruning (backward integrality).  Returns list of (S, dS, bits)."""
    mod = p ** prec
    out = []
    stack = [(S, dS, b, n0) for (S, dS, b) in roots]
    while stack:
        S, dS, b, k = stack.pop()
        if k == n1:
            out.append((S, dS, b))
            continue
        for bit in (0, 1):
            if bit:
                S2, dS2, b2 = (S + pi[k]) % mod, (dS + dpi[k]) % mod, b | (1 << k)
            else:
                S2, dS2, b2 = S, dS, b
            if v(S2, p, prec) >= Vc[k + 1]:
                stack.append((S2, dS2, b2, k + 1))
    return out


def initial_paths(pi, dpi, Vc, n0, p, prec):
    """All paths of length n0 alive at n0 (e_0 = 1)."""
    root = [(pi[0] % p ** prec, dpi[0] % p ** prec, 1)]
    if v(root[0][0], p, prec) < Vc[1]:
        return []
    return alive_paths(pi, dpi, Vc, 1, n0, root, p, prec)


def target(S, pin, Vn, p, prec):
    """tau = -S/pi_n as an integer mod p^(prec - Vn - something): returns (tau mod p^(prec-Vn)).  Requires
    v(S) >= Vn = v(pi_n)."""
    mod = p ** (prec - Vn)
    s = (S // p ** Vn) % mod
    u = (pin // p ** Vn) % mod
    return (-s * pow(u, -1, mod)) % mod


def composite_counts(x, n0, n2, K, p):
    """Exact counts m(t) = #{f in {0,1}^{n2-n0}: sum f_c pi_c(x)/pi_{n0}(x) = t mod p^K}, as a list."""
    mod = p ** K
    cnt = [0] * mod
    cnt[0] = 1
    y = 1
    for c in range(n0, n2):
        if c > n0:
            y = y * (x + c) % mod
        # element y_c = (x+n0+1)...(x+c)
        new = cnt[:]
        s = y % mod
        if s:
            for t in range(mod):
                if cnt[t]:
                    new[(t + s) % mod] += cnt[t]
        else:
            new = [2 * a for a in cnt]
        cnt = new
    return cnt


def band_L2_exact(cnt, D, K, p, total):
    """eps = p^K Coll_K - p^D Coll_D for the law cnt/total on Z/p^K (exact Fraction)."""
    collK = sum(a * a for a in cnt)
    md = p ** D
    fold = [0] * md
    for t, a in enumerate(cnt):
        fold[t % md] += a
    collD = sum(a * a for a in fold)
    return Fraction(p ** K * collK - p ** D * collD, total * total)
