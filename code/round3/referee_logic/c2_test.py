"""Round-3 logic referee: an independent, definition-level test of R3M's
Corollary A' (L = 0), Proposition B(ii) and Proposition C2 (note Props 11.10-11.13),
and of Proposition N (note Prop 11.12).

Everything is computed from the definitions, with none of R3M's structural lemmas:
  * a path e = (e_0=1, e_1, ...) is alive at j  iff  v_p(sum_{i<j} e_i pi_i(x')) >= V_j(x');
  * its slope is v_p(sum_{i<j} e_i pi_i'(x'));
  * Z0_j(x') = number of slope-0 paths of length j alive at j, found by a DFS over
    all 0/1 words (prefix pruning is valid because an alive path's prefixes are alive);
  * the cylinder C = x0 + p^m Z_p (m = V_n(x)) is sampled exhaustively: x' runs over
    x0 + p^m w + p^(m+D+D') r_w for every w mod p^(D+D') with a fresh random r_w, so
    the test also checks that nothing depends on the digits above m+D+D'.
Then, with c_j = p^{V_j}/2^j and exact rationals:
  (M)  mean_C c_N Z0_N = mean_C c_N' Z0_N' = c_n Z0_n                       (Cor A')
  (B)  mean_C (c_N Z0_N)^2 - (c_n Z0_n)^2 <= chi_W^2 (c_n Z0_n)^2, '=' if Z0_n = 1
  (C2) mean_C (c_N' Z0_N')^2 - mean_C (c_N Z0_N)^2 <= eps (c_n Z0_n)^2, '=' if Z0_n = 1,
       eps = p^(D+D') Coll_(D+D') - p^D Coll_D of the composite window [n, N')
  (N)  chi_W^2 >= (p-1) 4^-p.
Usage: python3 -I c2_test.py p SEED NSAMPLES n H H' [MAXCYL [ONLY_SINGLE=1]]
"""
import random
import sys
from fractions import Fraction


def vp(z, p, cap):
    if z == 0:
        return cap
    k = 0
    while z % p == 0:
        z //= p
        k += 1
    return k


def coll(elems, p, K):
    """sum_r nu(r)^2 for the uniform subset-sum law of elems mod p^K (exact)."""
    mod = p ** K
    dist = {0: 1}
    for y in elems:
        y %= mod
        nd = dict(dist)
        for r, c in dist.items():
            s = (r + y) % mod
            nd[s] = nd.get(s, 0) + c
        dist = nd
    tot = 2 ** len(elems)
    return Fraction(sum(c * c for c in dist.values()), tot * tot)


def slope0_counts(xp, p, PREC, stages, Nmax):
    mod = p ** PREC
    vals = [vp(xp + i, p, PREC) for i in range(1, Nmax + 1)]
    V = [0] * (Nmax + 1)
    for j in range(1, Nmax + 1):
        V[j] = V[j - 1] + vals[j - 1]
    pi = [1] * Nmax
    dpi = [0] * Nmax
    for j in range(1, Nmax):
        f = (xp + j) % mod
        dpi[j] = (dpi[j - 1] * f + pi[j - 1]) % mod
        pi[j] = (pi[j - 1] * f) % mod
    counts = {s: 0 for s in stages}
    # iterative DFS: state (length j, S, dS); e_0 = 1 is fixed
    stack = [(1, 1 % mod, 0)]
    while stack:
        j, S, dS = stack.pop()
        if vp(S, p, PREC) < V[j]:
            continue
        if j in counts and dS % p != 0:
            counts[j] += 1
        if j == Nmax:
            continue
        stack.append((j + 1, S, dS))
        stack.append((j + 1, (S + pi[j]) % mod, (dS + dpi[j]) % mod))
    return counts, V, max(vals)


def main():
    p, seed, nsamp, n, H, H2 = (int(a) for a in sys.argv[1:7])
    maxcyl = int(sys.argv[7]) if len(sys.argv) > 7 else 2000
    only_single = len(sys.argv) > 8 and sys.argv[8] == "1"
    rng = random.Random(seed)
    N, N2 = n + H, n + H + H2
    PREC = 3 * N2  # comfortably above V_{N'} + slack for these sizes
    stats = dict(tested=0, skip_hyp=0, skip_empty=0, skip_big=0, single=0,
                 M_ok=0, B_ok=0, B_eq=0, C2_ok=0, C2_eq=0, N_ok=0, const_ok=0)
    worst_C2 = Fraction(0)
    print(f"# c2_test p={p} seed={seed} samples={nsamp} n={n} N={N} N'={N2} PREC={PREC}")
    tries = 0
    while stats["tested"] < nsamp and tries < 400 * nsamp:
        tries += 1
        x = rng.randrange(p ** PREC)
        cnt, V, _ = slope0_counts(x, p, PREC, (n, N, N2), N2)
        m, D, D2 = V[n], V[N] - V[n], V[N2] - V[N]
        M2 = max(vp(x + i, p, PREC) for i in range(1, N2 + 1))
        if not (D + D2 <= m - M2 and M2 < m):
            stats["skip_hyp"] += 1
            continue
        if cnt[n] == 0 or (only_single and cnt[n] != 1):
            stats["skip_empty"] += 1
            continue
        if p ** (D + D2) > maxcyl:
            stats["skip_big"] += 1
            continue
        x0 = x % p ** m
        sN = Fraction(0); sN2 = Fraction(0); qN = Fraction(0); qN2 = Fraction(0)
        cn = Fraction(p ** V[n], 2 ** n)
        cN = Fraction(p ** (m + D), 2 ** N)
        cN2 = Fraction(p ** (m + D + D2), 2 ** N2)
        Zn = cnt[n]
        const_ok = True
        W = p ** (D + D2)
        for w in range(W):
            r = rng.randrange(p ** (PREC - m - D - D2))
            xp = x0 + p ** m * w + p ** (m + D + D2) * r
            c, Vp, _ = slope0_counts(xp, p, PREC, (n, N, N2), N2)
            if c[n] != Zn or Vp[n] != m or Vp[N] != m + D or Vp[N2] != m + D + D2:
                const_ok = False
            sN += cN * c[N]; sN2 += cN2 * c[N2]
            qN += (cN * c[N]) ** 2; qN2 += (cN2 * c[N2]) ** 2
        sN /= W; sN2 /= W; qN /= W; qN2 /= W
        # windows at x
        win = []
        prod = 1
        for j in range(n, N2):
            if j > n:
                prod *= (x + j)
            win.append(prod)
        chi2 = p ** D * coll(win[:H], p, D) - 1
        eps = p ** (D + D2) * coll(win, p, D + D2) - p ** D * coll(win, p, D)
        M0 = cn * Zn
        stats["tested"] += 1
        stats["const_ok"] += const_ok
        if sN == M0 and sN2 == M0:
            stats["M_ok"] += 1
        lhsB = qN - M0 * M0
        if lhsB <= chi2 * M0 * M0:
            stats["B_ok"] += 1
        lhsC = qN2 - qN
        if lhsC <= eps * M0 * M0:
            stats["C2_ok"] += 1
        if D >= 1 and chi2 >= Fraction(p - 1, 4 ** p):
            stats["N_ok"] += 1
        elif D == 0:
            stats["N_ok"] += 1
        ratio = lhsC / (eps * M0 * M0) if eps > 0 else Fraction(0)
        if Zn == 1:
            stats["single"] += 1
            stats["B_eq"] += (lhsB == chi2 * M0 * M0)
            stats["C2_eq"] += (lhsC == eps * M0 * M0)
        else:
            worst_C2 = max(worst_C2, ratio)
        print(f"x mod p^{m + D + D2}={x % p ** (m + D + D2)} m={m} D={D} D'={D2} M_N'={M2} "
              f"Z0_n={Zn} chi2={float(chi2):.4g} eps={float(eps):.4g} "
              f"C2 ratio={float(ratio):.4f} const={const_ok}")
    print("# summary:", stats, f"max C2 ratio over |P|>1: {float(worst_C2):.4f}")


if __name__ == "__main__":
    main()
