#!/usr/bin/env python3
"""Independent recomputation of Corollary P1 (track M4D, Theorem P / Corollary P1).

Written from the statement in data/round4/reports/M4D.md section 4 only (no code
reused from code/round4/M4D/).  Everything is exact (fractions.Fraction); floats
are used only for printing.

For each prime p in {7,11,13,17,19,23}:
  * H_t list (round-2 uniform certificates, note section 10.2), T = len(H_t),
    n0 = max H_t;
  * census delta_{G0}(p): both the 5-decimal value printed in note 4.7 and the
    exact count from archive/E/tree_p*.txt (passed in below; the counts are
    re-derived by census.c in this directory, see census.log);
  * b = sum_{p^k <= n0} ceil(n0/p^k), k1 = least k with p^k > n0,
    k0 = G0 - b + k1 (needs b <= G0);
  * the union bound n0 p^{-k0} and, as a cross-check, the EXACT Haar measure
    of {V_{n0} > G0};
  * B_p = delta_{G0} - 1e-5 - n0 p^{-k0} (as in the report, printed census value)
    and B_p^exact = delta_{G0}(exact) - n0 p^{-k0};
  * for eps in {0.01,0.05,0.1}: N = n0 + floor(eps p^{T+1}) (largest N with
    (N-n0) p^{-(T+1)} <= eps) and G = v_p(N!).
"""
from fractions import Fraction as F
import math, sys

CERT = {  # note.md section 10.2 table "uniform Cov(p,t,H_t)"
    7:  [4, 7, 19, 26, 28, 34],
    11: [5, 10, 18, 22, 30, 33],
    13: [6, 10, 19, 24, 32, 35, 39],
    17: [5, 11, 16, 25, 30, 34, 43],
    19: [5, 12, 17, 27, 31, 35],
    23: [7, 12, 18, 23, 33, 37],
}
# (G0, printed 5-decimal census value from note 4.7, exact survivor count mod p^G0 from archive/E)
CENSUS = {
    7:  (8, F(62394, 100000), 3596877),
    11: (6, F(69976, 100000), 1239663),
    13: (5, F(75454, 100000), 280157),
    17: (4, F(75692, 100000), 63219),
    19: (4, F(77792, 100000), 101379),
    23: (3, F(85617, 100000), 10417),
}
# Report's table (M4D.md section 4) to compare against
REPORT = {
    7:  dict(T=6, n0=34, G0=8, k0=5, B=0.62191, G=(1376, 6867, 13728)),
    11: dict(T=6, n0=33, G0=6, k0=5, B=0.69955, G=(19488, 97437, 194874)),
    13: dict(T=7, n0=39, G0=5, k0=4, B=0.75316, G=(679775, 3398877, 6797756)),
    17: dict(T=7, n0=43, G0=4, k0=3, B=0.74816, G=(4359848, 21799241, 43598483)),
    19: dict(T=6, n0=35, G0=4, k0=4, B=0.77764, G=(496595, 2482976, 4965952)),
    23: dict(T=6, n0=37, G0=3, k0=3, B=0.85312, G=(1547647, 7738240, 15476478)),
}
EPS = (F(1, 100), F(5, 100), F(1, 10))


def vfact(p, N):
    s, q = 0, p
    while q <= N:
        s += N // q
        q *= p
    return s


def exact_mu_V_gt(p, n0, G0):
    """Exact Haar measure of {x in Z_p : V_{n0}(x) = sum_{i<=n0} v(x+i) > G0}."""
    k1 = 1
    while p ** k1 <= n0:
        k1 += 1
    L = k1 - 1                     # levels k < k1 are determined by x mod p^L
    mod = p ** L
    tot = F(0)
    for r in range(mod):
        base = 0
        for k in range(1, k1):
            base += sum(1 for i in range(1, n0 + 1) if (r + i) % p ** k == 0)
        # candidates i with v(x+i) >= L (= k1-1): x+i == 0 mod p^L
        cand = sum(1 for i in range(1, n0 + 1) if (r + i) % mod == 0)
        # levels k >= k1 contribute #{k >= k1 : m* >= k} = max(0, m*-k1+1)
        need = G0 - base          # need max(0,m*-k1+1) >= need+1
        if need < 0:
            tot += F(1, mod)
        else:
            kk = need + k1        # m* >= kk ; P(m*>=kk | r) = cand * p^{-(kk-L)} (disjoint events)
            tot += F(1, mod) * cand * F(1, p ** (kk - L))
    return tot


def brute_mu_V_gt(p, n0, G0, L):
    """Brute force over x mod p^L (only valid if L is large enough that v(x+i) >= L
    contributes correctly; we treat v(x+i) >= L as the event and add its exact tail)."""
    cnt = F(0)
    mod = p ** L
    for x in range(mod):
        V = 0
        top = []
        for i in range(1, n0 + 1):
            y = (x + i) % mod
            if y == 0:
                top.append(i)
                continue
            v = 0
            while y % p == 0:
                y //= p
                v += 1
            V += v
        if not top:
            if V > G0:
                cnt += F(1, mod)
        else:
            # one i with v(x+i) >= L (at most one if p^L > n0); v = L + j with prob (1-1/p) p^{-j}
            assert len(top) == 1
            need = G0 + 1 - V      # need v >= need
            if need <= L:
                cnt += F(1, mod)
            else:
                cnt += F(1, mod) * F(1, p ** (need - L))
    return cnt


def main():
    ok = True
    print("p | T | n0 | b | k1 | G0 | k0 | union n0 p^-k0 | exact mu(V_n0>G0) | delta_G0 printed | delta_G0 exact | "
          "B_p (report formula) | B_p exact-census | report B_p")
    rows = {}
    for p, H in CERT.items():
        T = len(H)
        n0 = max(H)
        assert all(h + 1 < p ** (t + 1) for t, h in enumerate(H)), "H_t + 1 < p^t violated"
        G0, dprint, cnt = CENSUS[p]
        dex = F(cnt, p ** G0)
        b = sum(-(-n0 // p ** k) for k in range(1, 64) if p ** k <= n0)
        k1 = min(k for k in range(1, 64) if p ** k > n0)
        assert b <= G0
        k0 = G0 - b + k1
        ub = F(n0, p ** k0)
        ex = exact_mu_V_gt(p, n0, G0)
        assert ex <= ub, (p, ex, ub)
        B = dprint - F(1, 10 ** 5) - ub
        Bx = dex - ub
        # rounding check: printed census value within 1e-5 of exact
        assert abs(dprint - dex) <= F(5, 10 ** 6), (p, float(dprint - dex))
        assert B <= Bx
        rows[p] = (T, n0, B, Bx)
        print(f"{p} | {T} | {n0} | {b} | {k1} | {G0} | {k0} | {float(ub):.6e} | {float(ex):.6e} | "
              f"{float(dprint):.5f} | {float(dex):.10f} | {float(B):.7f} | {float(Bx):.7f} | {REPORT[p]['B']}")
        R = REPORT[p]
        for key, val in (("T", T), ("n0", n0), ("G0", G0), ("k0", k0)):
            if R[key] != val:
                print(f"  MISMATCH {key}: report {R[key]} mine {val}")
                ok = False
        if abs(float(B) - R["B"]) > 0.5e-5:
            print(f"  MISMATCH B_p: report {R['B']} mine {float(B):.7f}")
            ok = False
    print()
    print("p | eps | N = n0+floor(eps p^(T+1)) | loss (N-n0)p^-(T+1) | G = v_p(N!) | B_p - loss | report G")
    for p, (T, n0, B, Bx) in rows.items():
        for j, eps in enumerate(EPS):
            P = p ** (T + 1)
            N = n0 + math.floor(eps * P)
            loss = F(N - n0, P)
            assert loss <= eps and F(N + 1 - n0, P) > eps
            G = vfact(p, N)
            # also: largest G for which the bound B - eps is certified = v_p(N!) with this N
            print(f"{p} | {float(eps)} | {N} | {float(loss):.7f} | {G} | {float(B - loss):.6f} | {REPORT[p]['G'][j]}")
            if G != REPORT[p]["G"][j]:
                print("  MISMATCH G")
                ok = False
    print()
    # headline numbers in the report
    heads = [(7, F(1, 100), F(6119, 10000), 1376), (13, F(1, 100), F(7431, 10000), 679775),
             (13, F(1, 10), F(6531, 10000), 6790000)]
    for p, eps, val, Gmax in heads:
        T, n0, B, Bx = rows[p]
        P = p ** (T + 1)
        N = n0 + math.floor(eps * P)
        G = vfact(p, N)
        bound = B - F(N - n0, P)
        good = bound >= val and G >= Gmax
        print(f"headline: delta_G({p}) >= {float(val)} for G <= {Gmax}: bound at N={N} (G={G}) is {float(bound):.7f} -> {'OK' if good else 'FAIL'}")
        ok &= good
    # brute-force cross-check of exact_mu_V_gt on cases small enough to enumerate
    print()
    for (p, n0, G0, L) in [(7, 34, 8, 3), (7, 34, 6, 3), (11, 33, 6, 3), (13, 39, 5, 3), (7, 20, 4, 3), (5, 30, 9, 4)]:
        a = exact_mu_V_gt(p, n0, G0)
        bb = brute_mu_V_gt(p, n0, G0, L)
        print(f"crosscheck exact mu(V_{n0}>{G0}) p={p}: formula {float(a):.6e}, brute(mod p^{L}) {float(bb):.6e} -> {'OK' if a == bb else 'MISMATCH'}")
        ok &= (a == bb)
    print("ALL OK" if ok else "SOME MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
