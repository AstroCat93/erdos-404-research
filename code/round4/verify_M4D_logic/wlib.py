"""wlib.py -- helper library for the logic check of M4D section 3 (Lemmas W1-W3, Prop W4, Cor W5, Thm W6).

Written for this check from the statements in data/round4/reports/M4D.md section 3 and
data/round3/reports/R3M.md sections 1-5.  It shares no code with code/round4/M4D/.

Conventions (R3M section 1):
  pi_j(x) = (x+1)...(x+j);  V_n = v(pi_n(x));  M_n = max_{i<=n} v(x+i)  (the MAX VALUATION, never the functional).
  A path of length n is an int bitmask e with bit 0 set; S_e(x) = sum_{j<n} e_j pi_j(x).
  e alive at n  <=>  v(S_e(x)) >= V_n;  slope = v(S_e'(x)).
All p-adic numbers are Python integers reduced mod p^prec.  Test points x are nonnegative integers, which
are genuine points of Z_p and never negative integers, so every valuation below is exact as long as it is
< prec (asserted).
"""
from fractions import Fraction
import cmath


def vp(a, p, prec):
    """v_p(a mod p^prec); returns prec for 0 (caller asserts it never matters)."""
    mod = p ** prec
    a %= mod
    if a == 0:
        return prec
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k


def prods(x, N, p, prec):
    """pi[j], dpi[j] mod p^prec (j=0..N) and vals[i]=v(x+i) (i=1..N, vals[0]=0)."""
    mod = p ** prec
    pi = [1] * (N + 1)
    dpi = [0] * (N + 1)
    vals = [0] * (N + 1)
    for j in range(1, N + 1):
        pi[j] = pi[j - 1] * (x + j) % mod
        dpi[j] = (dpi[j - 1] * (x + j) + pi[j - 1]) % mod
        vals[j] = vp(x + j, p, prec)
        assert vals[j] < prec // 2, "valuation too close to precision"
    return pi, dpi, vals


def Vof(vals, n):
    return sum(vals[1:n + 1])


def Mof(vals, n):
    return max(vals[1:n + 1]) if n >= 1 else 0


def S_and_dS(bits, n, pi, dpi, mod):
    S = 0
    dS = 0
    for j in range(n):
        if (bits >> j) & 1:
            S += pi[j]
            dS += dpi[j]
    return S % mod, dS % mod


def grow(bits_list, start, N, x, p, prec, pi=None, dpi=None, vals=None):
    """All extensions to length N, alive at N, of the given paths of length `start`
    (each assumed alive at `start`).  Depth-first, one digit at a time, pruning with the
    converse of (F2) applied one step at a time (a prefix of a path alive at k+1 is alive at k).
    Returns list of (bits, S mod p^prec, S' mod p^prec)."""
    mod = p ** prec
    if pi is None:
        pi, dpi, vals = prods(x, N, p, prec)
    Vc = [0] * (N + 1)
    for j in range(1, N + 1):
        Vc[j] = Vc[j - 1] + vals[j]
    out = []
    stack = []
    for b in bits_list:
        S, dS = S_and_dS(b, start, pi, dpi, mod)
        stack.append((b, S, dS, start))
    while stack:
        b, S, dS, k = stack.pop()
        if k == N:
            out.append((b, S, dS))
            continue
        # digit 0
        if vp(S, p, prec) >= Vc[k + 1]:
            stack.append((b, S, dS, k + 1))
        S1 = (S + pi[k]) % mod
        if vp(S1, p, prec) >= Vc[k + 1]:
            stack.append((b | (1 << k), S1, (dS + dpi[k]) % mod, k + 1))
    return out


def alive_slope0(x, n, p, prec):
    """slope-0 paths alive at n, as bitmasks (e_0 = 1)."""
    pi, dpi, vals = prods(x, n, p, prec)
    if vals[1] > 0:  # path (1) alive at 1 iff v(1) >= v(x+1)
        return []
    res = grow([1], 1, n, x, p, prec, pi, dpi, vals)
    return [b for (b, S, dS) in res if vp(dS, p, prec) == 0]


def win_elems(x, n, N, modulus):
    """y_i = pi_{n+i}/pi_n = prod_{s=1}^i (x+n+s), 0<=i<N-n, mod modulus."""
    ys = []
    y = 1
    for i in range(N - n):
        ys.append(y % modulus)
        y = y * (x + n + i + 1) % modulus
    return ys


def win_unit(x, n, N, p, modulus):
    """u = pi_N/(p^D pi_n) mod modulus (a unit)."""
    u = 1
    for i in range(n + 1, N + 1):
        a = x + i
        while a % p == 0:
            a //= p
        u = u * a % modulus
    return u


def subset_sums(ys, modulus):
    """list s[f] (f bitmask over len(ys)) of sum_i f_i ys[i] mod modulus."""
    H = len(ys)
    s = [0] * (1 << H)
    for f in range(1, 1 << H):
        low = f & (-f)
        i = low.bit_length() - 1
        s[f] = (s[f ^ low] + ys[i]) % modulus
    return s


def law(sums, q, modulus):
    """weighted law: dict r -> sum q[f] over f with sums[f] = r mod modulus."""
    d = {}
    for f, s in enumerate(sums):
        if q[f]:
            r = s % modulus
            d[r] = d.get(r, 0) + q[f]
    return d


def coll(d):
    return sum(c * c for c in d.values())


def fine_tilde(sums, q, p, D, Dp):
    """eps~^q = p^(D+D') Coll_{D+D'}(mu^q) - p^D Coll_D(mu^q)  (exact if q is Fraction)."""
    K = D + Dp
    return p ** K * coll(law(sums, q, p ** K)) - p ** D * coll(law(sums, q, p ** D))


def chi2(sums, q, p, D):
    return p ** D * coll(law(sums, q, p ** D)) - 1


def composite_fine(sums, q, sums2, q2, u, p, D, Dp):
    """eps^{q,q'} = p^K Coll_K(nu) - p^D Coll_D(nu), nu = law of Q_f + p^D u Q'_{f'} mod p^K."""
    K = D + Dp
    l1 = law(sums, q, p ** K)
    l2 = law(sums2, q2, p ** Dp)
    nu = {}
    for r1, c1 in l1.items():
        for r2, c2 in l2.items():
            s = (r1 + p ** D * u * r2) % p ** K
            nu[s] = nu.get(s, 0) + c1 * c2
    nuD = {}
    for s, c in nu.items():
        nuD[s % p ** D] = nuD.get(s % p ** D, 0) + c
    return p ** K * coll(nu) - p ** D * coll(nuD)


def fourier(d, zeta, modulus):
    """hat mu(zeta) = sum_r d[r] e(-zeta r / modulus) (complex float)."""
    t = 0j
    for r, c in d.items():
        t += float(c) * cmath.exp(-2j * cmath.pi * ((zeta * r) % modulus) / modulus)
    return t


def F_fibre(sums, q, p, D, k, xi, u):
    """F^q(xi) = sum_{zeta mod p^(D+k), zeta = xi u^{-1} mod p^k} |hat mu^q_{D+k}(zeta)|^2 (float)."""
    K = D + k
    d = law(sums, q, p ** K)
    c = xi * pow(u, -1, p ** k) % p ** k if k > 0 else 0
    tot = 0.0
    for z in range(c, p ** K, p ** k if k > 0 else 1):
        tot += abs(fourier(d, z, p ** K)) ** 2
    return tot


def F_table(sums, q, p, D, k, u):
    """dict xi -> F^q(xi) for all xi mod p^k, via ONE numpy FFT of the law mod p^(D+k) (float).
    numpy.fft.fft(a)[z] = sum_r a[r] exp(-2 pi i z r / P), i.e. hat mu(z) with the sign convention of
    M4D section 3.  Cross-validated against the direct sum F_fibre in w1_abstract.py (see 'FFT' check)."""
    import numpy as np
    K = D + k
    PK = p ** K
    arr = np.zeros(PK)
    for r, c in law(sums, q, PK).items():
        arr[r] = float(c)
    pw = np.abs(np.fft.fft(arr)) ** 2
    pk = p ** k
    uinv = pow(u, -1, pk) if k > 0 else 0
    out = {}
    for xi in range(pk):
        c = xi * uinv % pk if k > 0 else 0
        out[xi] = float(pw[c::pk].sum()) if k > 0 else float(pw.sum())
    return out


def lifts_of(sums, p, D, Dp):
    """dict r (mod p^D) -> dict s (mod p^(D+D')) -> list of f."""
    K = D + Dp
    out = {}
    for f, s in enumerate(sums):
        s %= p ** K
        out.setdefault(s % p ** D, {}).setdefault(s, []).append(f)
    return out


def hm_and_qstar(sums, p, D, Dp):
    """Corollary W5: returns (m, qstar, a) with a[r] = p^D'/|Lift(r)| - 1 (None = infinity)."""
    L = lifts_of(sums, p, D, Dp)
    a = {}
    for r in range(p ** D):
        k = len(L.get(r, {}))
        a[r] = None if k == 0 else Fraction(p ** Dp, k) - 1
    complete = [r for r in a if a[r] == 0]
    if complete:
        m = Fraction(0)
        nu = {r: Fraction(1, len(complete)) for r in complete}
    else:
        inv = sum(1 / a[r] for r in a if a[r] is not None)
        m = Fraction(p ** D) / inv
        nu = {r: (1 / a[r]) / inv for r in a if a[r] is not None}
    qs = [Fraction(0)] * len(sums)
    for r, w in nu.items():
        Lr = L[r]
        for s, fl in Lr.items():
            for f in fl:
                qs[f] = w / (len(Lr) * len(fl))
    return m, qs, a


def rand_prob(rnd, n, zero_frac=0.0, hi=9):
    raw = [0 if rnd.random() < zero_frac else rnd.randint(1, hi) for _ in range(n)]
    if sum(raw) == 0:
        raw[rnd.randrange(n)] = 1
    t = sum(raw)
    return [Fraction(c, t) for c in raw]
