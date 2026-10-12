# Computer-assisted check for the explicit-rate theorem on a residue class C of Z_2.
# For C = {x = -lstar + 2^s * eta : eta odd, s in [smin, sdead)} (all other v(x+l), l <= n0, are then fixed),
# enumerate eta mod 2^R (results must not depend on R or on random higher digits), and for every path valid
# through n0 compute kappa_{n0} = v(B_{n0}(x,x)), test 1-stability, and accumulate
#    I_{n0}(C) = int_C N_{n0}(x) 2^{P_{n0}(x)-n0} dx = sum_s 2^{-s-1} * 2^{P-n0} * avg_eta N_{n0}.
# Points with s >= sdead have no path valid through lstar (shadow argument, gamma_2(lstar) < sdead).
import random, sys
BIG = 1 << 400
def v2(n):
    n %= BIG
    return 400 if n == 0 else (n & -n).bit_length() - 1
def run_paths(x, n0):
    # returns list of (gamma mod 2^prec, B mod 2^64) for all valid paths through n0
    pop = [(0, 0, 1)]  # (gamma, B, pi_{n-1} mod 2^64) ; gamma_0 = 0
    prec = 400; out = []
    states = [(0, 0)]
    pi = 1
    for n in range(1, n0 + 1):
        d = v2(x + n); newprec = prec - d
        u = ((x + n) % BIG) >> d; inv = pow(u % (1 << newprec), -1, 1 << newprec)
        new = []
        for (g, B) in states:
            for e in ((1,) if n == 1 else (0, 1)):
                t = (g + e) % (1 << prec)
                if d and (t & ((1 << d) - 1)): continue
                gn = ((t >> d) * inv) % (1 << newprec)
                new.append((gn, (B + gn * pi) % (1 << 64)))
        states = new; prec = newprec; pi = (pi * (x + n)) % (1 << 64)
    return states
def check(cls_name, mod, res, lstar, smin, sdead, n0, R, kap_expected, seed=1):
    rnd = random.Random(seed)
    I = 0.0; bad = 0; allk = set()
    for s in range(smin, sdead):
        tot = 0; cnt = 0
        for eta in range(1, 1 << R, 2):
            x = (-lstar + ((eta + (rnd.getrandbits(80) << R)) << s)) % BIG
            if x % mod != res: continue
            env = [v2(x + l) for l in range(1, n0 + 1)]
            if v2(x + lstar) != s: continue
            P = sum(env); M = max(env)
            st = run_paths(x, n0)
            for (g, B) in st:
                k = v2(B) if B else 64
                allk.add(k)
                if not (P - k >= k + M + 1): bad += 1
            tot += len(st); cnt += 1
        if cnt == 0: continue
        avg = tot / cnt
        # measure of {x in C : v(x+lstar) = s} = 2^{-s-1} (if that sphere lies in C)
        P_s = sum(v2(((-lstar + (1 << s)) % BIG) + l) for l in range(1, n0 + 1))
        I += 2.0 ** (-s - 1) * 2.0 ** (P_s - n0) * avg
        print(f"  {cls_name} s={s} samples={cnt} avg N_{n0}={avg:.6f} P={P_s}")
    print(f"{cls_name}: R={R} kappa values seen {sorted(allk)} (expected {kap_expected}), unstable paths: {bad}, I_{n0} = {I!r}")
    return I
if __name__ == "__main__":
    for R in (10, 12):
        check("C0 = 0 mod 8", 8, 0, 8, 3, 9, 8, R, 1)
        check("C2 = 2 mod 8", 8, 2, 6, 3, 7, 12, R, 3)
        check("C6 = 6 mod 16", 16, 6, 10, 4, 11, 10, R, 3)
