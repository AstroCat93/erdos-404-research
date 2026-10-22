#!/usr/bin/env python3
"""Finite certificate for uniform slopes on a residue class (R3Q report, Lemma 3'; computer-assisted).

Claim checked: for every x in r + 2^a Z_2 and every path e with v(S_e(x)) >= c, v(S_e'(x)) = lam0.
Reduction to a finite check (proved in the report):
  * choose J with V_J(x) >= c for all x in the class (a lower bound for V_J from the valuations
    v(x+i), i <= J, that are determined by x mod 2^a, plus 1 for each i that is 0 mod 2^a ... see vmin);
    then S_e(x) mod 2^c depends only on (e_1..e_{J-1}) and on x mod 2^c;
  * choose J' with v(pi_j'(x)) >= lam0+1 for all j >= J' and all x in the class (bound V_j - M_j
    from the determined valuations); then S_e'(x) mod 2^{lam0+1} depends only on (e_1..e_{J'-1})
    and on x mod 2^{lam0+1};
  * so it suffices to check all x mod 2^c in the class and all prefixes of length max(J,J').
The determined-valuation bounds are computed exactly from the class: v(x+i) = v(r+i) if v(r+i) < a,
else v(x+i) >= a (unknown above).
usage: slope_cert.py r a c lam0
"""
import sys

def v2(a): return (a & -a).bit_length() - 1 if a else 10**9

def vmin(r, a, i):
    """Lower bound for v(x+i) valid for all x = r mod 2^a, and whether it is exact."""
    t = v2(r + i)
    return (t, True) if t < a else (a, False)

def main():
    r, a, c, lam0 = (int(t) for t in sys.argv[1:5])
    # J: smallest J with sum_{i<=J} vmin >= c  (then V_j >= c for all j >= J)
    s = 0; J = None
    for i in range(1, 10**4):
        s += vmin(r, a, i)[0]
        if s >= c:
            J = i; break
    # J': smallest J' such that for all j >= J': V_j - M_j >= lam0 + 1.  Lower bound for V_j - M_j:
    # sum of vmin over i <= j minus the largest unbounded-or-max term -> use: sum of exact vmin over i<=j
    # excluding every inexact index (those may carry the maximum), and excluding the largest exact one.
    def lowVM(j):
        vals = [vmin(r, a, i) for i in range(1, j + 1)]
        exact = sorted([t for t, ex in vals if ex])
        inexact = [t for t, ex in vals if not ex]
        if inexact:
            # the maximum may be an inexact index: drop one inexact term (others contribute >= a each)
            return sum(exact) + a * (len(inexact) - 1)
        return sum(exact[:-1]) if exact else 0
    Jp = None
    for j in range(1, 10**4):
        if all(lowVM(jj) >= lam0 + 1 for jj in range(j, j + 2 ** (a + 2))):
            Jp = j; break
    L = max(J, Jp)
    print(f"class {r} mod 2^{a}: V_j >= {c} for j >= J={J}; v(pi_j') >= {lam0+1} for j >= J'={Jp}; prefix length {L}")
    MODc = 1 << c
    bad = 0; alive_count = 0; classes = 0
    for xr in range(r % (1 << a), MODc, 1 << a):
        classes += 1
        # pi_j(x) mod 2^c and pi_j'(x) mod 2^c for j < L
        p0, p1 = [1], [0]
        for j in range(1, L):
            p1.append((p1[-1] * (xr + j) + p0[-1]) % MODc)
            p0.append(p0[-1] * (xr + j) % MODc)
        # enumerate prefixes e_1..e_{L-1} by DFS with pruning on S mod 2^c only at the end
        # (2^(L-1) is small for the classes certified here)
        for mask in range(1 << (L - 1)):
            S = 1; Sp = 0
            m = mask; j = 1
            while m:
                if m & 1:
                    S += p0[j]; Sp += p1[j]
                m >>= 1; j += 1
            if S % MODc == 0:
                alive_count += 1
                if v2(Sp % MODc) != lam0:
                    bad += 1
                    if bad < 5:
                        print("COUNTEREXAMPLE x mod 2^c =", xr, "prefix mask", mask, "v(S') =", v2(Sp % MODc))
    print(f"x-classes={classes} prefixes per class={1 << (L-1)} prefixes with S=0 mod 2^{c}: {alive_count} "
          f"violations={bad}  -> {'CERTIFIED' if bad == 0 else 'FAILED'}")

if __name__ == "__main__":
    main()
