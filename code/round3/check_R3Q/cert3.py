#!/usr/bin/env python3
"""Adversarial check of R3Q Lemma 3 (slope certificates), written independently of code/round3/R3Q.

Method: dual numbers.  For a residue x mod 2^c we carry (pi_j(x), pi_j'(x)) mod 2^c through the
recurrence pi_j = pi_{j-1} * (x+j)  (so pi_j' = pi_{j-1}' (x+j) + pi_{j-1}), then enumerate every word
e = (1, e_1, ..., e_{n0-1}) as an integer bitmask and accumulate S_e(x), S_e'(x) mod 2^c by a subset-sum
table (dynamic programming over the bits, no per-word loop over j).

Checks (exactly as stated in the report, data/round3/reports/R3Q.md, Lemma 3 finite checks (a)-(e)):
  (a) x = 0 mod 8,  x mod 2^4,  n0 = 6 : 2^4  | S_e(x)  =>  v(S_e'(x)) = 1
  (b) x = 2 mod 16, x mod 2^7,  n0 = 8 : 2^7  | S_e(x)  =>  v(S_e'(x)) = 3
  (c) x = 6 mod 16, x mod 2^11, n0 = 10: 2^11 | S_e(x)  =>  v(S_e'(x)) = 3
  (d) x = 10 mod 16, x mod 2^7, n0 = 6 : no e with 2^7 | S_e(x)
  (e) x = 4 mod 8,  x mod 2^4,  n0 = 4 : no e with 2^4 | S_e(x)
and, separately, the valuation facts used in the reduction (V_{n0}, M_{n0}, V_{n0}-M_{n0}) by brute force over
x mod 2^20 in each class (v(x+i) capped at 20 is exact there for the small i involved, except where it is
>= 20, which we report as '>=').
Also a stronger sanity check: (a)-(c) re-run with one and two extra bits of x (modulus 2^{c+1}, 2^{c+2}),
which must give the same verdicts (S mod 2^c and S' mod 2^{lambda+1} only depend on x mod 2^c)."""
import sys, time

def v2(a, cap):
    if a == 0: return cap
    return min((a & -a).bit_length() - 1, cap)

def tables(x, n0, mod):
    """pi_j(x), pi_j'(x) mod `mod` for j = 0..n0-1 via dual numbers."""
    p, dp = 1, 0
    P, DP = [1], [0]
    for j in range(1, n0):
        p, dp = (p * (x + j)) % mod, (dp * (x + j) + p) % mod
        P.append(p); DP.append(dp)
    return P, DP

def run(name, cls_r, cls_m, c, n0, lam, extra=0):
    modx = 1 << (c + extra)
    mod = 1 << c
    qual = viol = 0
    for x in range(cls_r, modx, cls_m):
        P, DP = tables(x, n0, mod)
        # subset sums over bits 1..n0-1, with e_0 = 1 (pi_0 = 1, pi_0' = 0)
        S = [1]; D = [0]
        for j in range(1, n0):
            S = S + [(s + P[j]) % mod for s in S]
            D = D + [(d + DP[j]) % mod for d in D]
        for s, d in zip(S, D):
            if s % mod == 0:
                qual += 1
                if lam is None or v2(d, c) != lam:
                    viol += 1
    return qual, viol

def env_check():
    """V_{n0}, M_{n0} for each class, brute force over x mod 2^20."""
    out = []
    for name, r, m, n0 in (("C0", 0, 8, 6), ("C2", 2, 16, 8), ("C6", 6, 16, 10), ("C10", 10, 16, 6), ("C4", 4, 8, 4)):
        Vs, Ms, VMs = set(), set(), set()
        for x in range(r, 1 << 20, m):
            vs = [v2(x + i, 20) for i in range(1, n0 + 1)]
            V, M = sum(vs), max(vs)
            Vs.add(V); Ms.add(M); VMs.add(V - M)
        out.append(f"{name}: n0={n0} min V={min(Vs)} max V={max(Vs)} | min M={min(Ms)} max M={max(Ms)} | V-M in {sorted(VMs)[:6]}{'...' if len(VMs)>6 else ''}")
    return out

if __name__ == "__main__":
    t0 = time.time()
    checks = [("a", 0, 8, 4, 6, 1), ("b", 2, 16, 7, 8, 3), ("c", 6, 16, 11, 10, 3),
              ("d", 10, 16, 7, 6, None), ("e", 4, 8, 4, 4, None)]
    allok = True
    for extra in (0, 1, 2):
        for name, r, m, c, n0, lam in checks:
            q, vi = run(name, r, m, c, n0, lam, extra)
            ok = (vi == 0) if lam is not None else (q == 0)
            allok &= ok
            print(f"({name}) x={r} mod {m}, x mod 2^{c + extra}, n0={n0}: qualifying (word, x-residue) pairs={q} "
                  f"violations={vi if lam is not None else q} {'OK' if ok else 'FAIL'}")
    for line in env_check():
        print(line)
    print("ALL OK" if allok else "SOME CHECK FAILED", f"wall {time.time() - t0:.1f} s")
