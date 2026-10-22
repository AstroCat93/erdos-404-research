#!/usr/bin/env python3
"""s3_check.py (2026-10-21) -- independent exact check of Theorem S3 (exact fibre criterion at the final gate) and of
Theorem S2(iv) (the last block's normalised subset sums are the universal set V_p = (p-1)! Sigma(E_p) mod p^t).
For small (p, t, H = pH') and every unit class K' mod p^c:
  (1) direct: do the 2^H subset sums of y_i(K') = prod_{s<=i}(p^t K' - (H-s)), i<H, cover Z/p^M, M = t + v_p((H-1)!) ?
  (2) via S3: R = subset sums of the first H-p elements mod p^M; u = y_{H-p}/p^c; B_T = {(r-T)/p^c mod p^t : r in R, r = T mod p^c};
      criterion: for every T mod p^c, B_T + u*V_p = Z/p^t, with V_p = {sum_{u in S} (p-1)! (-1)^u / u! : S subset of [0,p)} (integers).
  (3) S2(iv): the set {y_{H-p+r}/y_{H-p} subset sums mod p^t} equals V_p mod p^t.
Reports any disagreement.  Uses exact integers only.  Also reports the number of missed residues in (1) and in (2) (sum over fibres)."""
import sys
from math import factorial
def vfac(n, p):
    s = 0
    while n:
        n //= p; s += n
    return s
def subset_sums_mod(elems, m):
    S = {0}
    for e in elems:
        e %= m
        S = S | {(x + e) % m for x in S}
    return S
def check(p, t, Hp):
    H = p * Hp
    c = vfac(H - 1, p); M = t + c; pM = p ** M; pt = p ** t; pc = p ** c
    # universal gate set V_p (integers)
    Ep = [((-1) ** u) * (factorial(p - 1) // factorial(u)) for u in range(p)]
    Vp = subset_sums_mod(Ep, pt)
    units = [K for K in range(1, pc) if K % p] if c > 0 else [1]
    out = []
    for K in units:
        X = p ** t * K
        y = [1]
        for i in range(1, H):
            y.append(y[-1] * (X - (H - i)))
        # (1) direct
        full = subset_sums_mod(y, pM)
        miss_direct = pM - len(full)
        # (3) last block normalised
        yb = y[H - p]
        assert yb % pc == 0 and (yb // pc) % p != 0, "last block valuation != c"
        u = (yb // pc) % pt
        blk = []
        for r in range(p):
            q, rem = divmod(y[H - p + r], yb)
            assert rem == 0
            blk.append(q % pt)
        Wset = subset_sums_mod(blk, pt)
        s2ok = (Wset == Vp)
        # (2) fibre criterion
        R = subset_sums_mod(y[:H - p], pM)
        fib = {}
        for r in R:
            T = r % pc
            fib.setdefault(T, set()).add(((r - T) // pc) % pt)
        uV = {(u * v) % pt for v in Vp}
        miss_fib = 0
        for T in range(pc):
            BT = fib.get(T, set())
            cov = {(b + v) % pt for b in BT for v in uV}
            miss_fib += pt - len(cov)
        ok = (miss_direct == 0) == (miss_fib == 0)
        out.append((K, miss_direct, miss_fib, s2ok, ok))
    return c, M, out
if __name__ == "__main__":
    cases = [(3, 2, 2), (3, 2, 3), (3, 3, 2), (3, 3, 3), (3, 3, 4), (3, 4, 3), (5, 2, 2), (5, 2, 3), (5, 3, 2), (5, 3, 3), (5, 3, 4), (5, 4, 3), (7, 2, 2), (7, 2, 3), (7, 3, 3), (11, 2, 2), (11, 2, 3), (13, 2, 2)]
    bad = 0
    for (p, t, Hp) in cases:
        c, M, out = check(p, t, Hp)
        nK = len(out); ncov = sum(1 for o in out if o[1] == 0)
        agree = all(o[4] for o in out); s2 = all(o[3] for o in out)
        same_count = all(o[1] == o[2] for o in out)
        print(f"p={p} t={t} H={p*Hp} c={c} M={M}: classes={nK} covered(direct)={ncov}  S3 agrees on every class: {agree}  "
              f"miss counts equal (direct vs sum over fibres): {same_count}  S2(iv) last block == V_p mod p^t: {s2}  "
              f"[K, miss_direct, miss_fibres]={[(o[0], o[1], o[2]) for o in out][:6]}{'...' if nK > 6 else ''}")
        if not (agree and s2): bad += 1
    print("S3/S2(iv) CHECK:", "ALL PASSED" if bad == 0 else f"{bad} FAILURES")
