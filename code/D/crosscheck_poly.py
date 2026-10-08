#!/usr/bin/env python3
"""Independent check of the C c-recursion code: decide g(a,p) >= G with the polynomial
subset-sum form 1 + sum_{b in B} P_b(a) == 0 mod p^G (P_b(x) = (x+1)...(x+b)), using a pruned
residue DP over b (no c-recursion, no factorials).  Compare exact g (capped) with ./gvalp."""
import random, subprocess, sys


def vp(n, p):
    if n == 0:
        return 10 ** 9
    v = 0
    while n % p == 0:
        n //= p; v += 1
    return v


def reach(a, p, G):
    mod = p ** G
    # weights P_b(a) mod p^G and exact valuations v_p(P_b(a)) (a >= 1 so P_b(a) != 0)
    S = {1 % mod}
    Pb = 1
    b = 0
    while True:
        b += 1
        Pb = Pb * (a + b)
        vb = vp(Pb, p)
        # before adding term b, partial sums must be 0 mod p^{min(G, v(P_b))}
        m = p ** min(G, vb)
        S = {s for s in S if s % m == 0}
        if not S:
            return False
        if vb >= G:
            return 0 in S
        w = Pb % mod
        S = S | {(s + w) % mod for s in S}


def g_poly(a, p, cap):
    G = 0
    while G < cap and reach(a, p, G + 1):
        G += 1
    return G


if __name__ == "__main__":
    p = int(sys.argv[1]); cap = int(sys.argv[2]); n = int(sys.argv[3]); seed = int(sys.argv[4])
    rnd = random.Random(seed)
    As = [rnd.randrange(1, p ** cap) for _ in range(n)]
    out = subprocess.run(["./gvalp", str(p), str(cap)] + [str(a) for a in As], capture_output=True, text=True).stdout.split("\n")
    bad = 0
    for a, line in zip(As, out):
        gc = int(line.split("g=")[1].split()[0])
        gp = g_poly(a, p, cap)
        if gc != gp:
            bad += 1
            print("MISMATCH", a, gc, gp)
    print(f"p={p} cap={cap} samples={n} mismatches={bad}")
