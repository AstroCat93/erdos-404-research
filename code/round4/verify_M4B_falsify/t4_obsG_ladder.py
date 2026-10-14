"""t4_obsG_ladder.py --
(a) Observation G (used in the proof of B1' for Q_j < infinity): if v(x+i) = s >= 1, V_n > s and e is a
    slope-0 path alive at n, then v(S_{e|i}(-i)) = s; hence Z0_n = 0 when p^s > e (i-1)!.
    Tested on explicit path lists at forced gates x = -i + p^s u (and random x).
(b) The bound used in B1': on {Z0_n != 0}, M_n <= log_p(e (n-1)!) and c_n Z0_n <= p^{V_n}/2.
(c) The example rule of M4B section 2 (C'-ladder start for horizon Tmax found with truncated
    valuations min(v(x+i), m_{l-1})): it is a function of x mod p^{m_{l-1}}, and on the event
    {M_{n_{l+1}+Tmax} < m_{l-1}} the truncated ladder property equals the true one.
Usage: python3 t4_obsG_ladder.py SEED NX"""
import sys, random, math
from fz_lib import *

seed, NX = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
R = 60
S = dict(paths=0, gates=0, G_fail=0, kill_tests=0, kill_fail=0, Mb_tests=0, Mb_fail=0,
         lad_tests=0, lad_fail=0, lad_exact_tests=0, lad_exact_fail=0, lad_func_fail=0)

for p in (3, 5, 7):
    for _ in range(NX):
        n = rng.randrange(2 * p, 2 * p + 10)
        i = rng.randrange(1, n + 1)
        s = rng.randrange(1, 9)
        X = (-i + p ** s * (1 + p * rng.randrange(p ** 30))) % p ** R if rng.random() < 0.8 else rng.randrange(p ** R)
        vl = vals(X, p, n); V, M = prefix(vl)
        if V[n] > 20:
            continue
        try:
            al = enum_alive(X, p, n, limit=60000)
        except RuntimeError:
            continue
        slope0 = [b for b, Sv, Sd in al if Sd % p]
        # (a) path-level statement for every gate position
        for b in slope0:
            S['paths'] += 1
            for ii in range(1, n + 1):
                si = vl[ii]
                if si >= 1 and V[n] > si:
                    S['gates'] += 1
                    val = sum(b[j] * math.prod(-ii + t for t in range(1, j + 1)) for j in range(ii))
                    if vp(val, p) != si:
                        S['G_fail'] += 1; print("FAIL ObsG", p, X, n, ii, si, b)
        # consequence: Z0 = 0 at deep gates
        deep = any(vl[ii] >= 1 and V[n] > vl[ii] and p ** vl[ii] > math.e * math.factorial(ii - 1) for ii in range(1, n + 1))
        if deep:
            S['kill_tests'] += 1
            if slope0:
                S['kill_fail'] += 1; print("FAIL ObsG kill", p, X, n)
        # (b) bound used in B1'
        if slope0:
            S['Mb_tests'] += 1
            cz = c_n(n, V[n], p) * len(slope0)
            if not (p ** M[n] <= math.e * math.factorial(n - 1) and cz <= Fraction(p ** V[n], 2)):
                S['Mb_fail'] += 1; print("FAIL M bound", p, X, n)
    print(f"RESULT p={p} cumulative {S}")


# (c) the M4B ladder rule
def ladder_rule(r, m, nl, p, rr, R_, Cp, Tmax):
    """least n >= ceil(rr*nl) that is a Cp-ladder point for horizon Tmax w.r.t. truncated valuations;
       else ceil(rr*nl)+R_.  Uses only r = x mod p^m."""
    start = math.ceil(rr * nl)
    tv = trunc_vals(r, m, p, start + R_ + Tmax + 1)
    for n in range(start, start + R_):
        dv = 0; ok = True
        for d in range(1, Tmax + 1):
            dv += tv[n + d]
            if Fraction(p ** dv, 2 ** d) > Cp:
                ok = False; break
        if ok:
            return n, True
    return start + R_, False


def true_ladder(X, p, n, Cp, Tmax):
    vl = vals(X, p, n + Tmax)
    dv = 0
    for d in range(1, Tmax + 1):
        dv += vl[n + d]
        if Fraction(p ** dv, 2 ** d) > Cp:
            return False
    return True


for p in (3, 5, 7):
    for _ in range(NX):
        X = rng.randrange(p ** R)
        if rng.random() < 0.4:
            k = rng.randrange(1, 80); s = rng.randrange(1, 6)
            X = (-k + p ** s * rng.randrange(1, p ** 30)) % p ** R
        nprev = 2 * p + rng.randrange(0, 10); nl = nprev + rng.randrange(2, 10)
        mprev = prefix(vals(X, p, nprev))[0][nprev]
        Tmax = rng.randrange(4, 20); Cp = Fraction(rng.choice([1, 2, 4]))
        n2, found = ladder_rule(X % p ** mprev, mprev, nl, p, 1.25, 30, Cp, Tmax)
        S['lad_tests'] += 1
        # function of x mod p^{m_{l-1}}: lifts give the same answer
        for _ in range(3):
            Y = X + p ** mprev * rng.randrange(p ** 25)
            if ladder_rule(Y % p ** mprev, mprev, nl, p, 1.25, 30, Cp, Tmax)[0] != n2:
                S['lad_func_fail'] += 1; print("FAIL ladder rule not G_{l-1}-measurable", p, X)
        vl = vals(X, p, n2 + Tmax); V, M = prefix(vl)
        if found and M[n2 + Tmax] < mprev:
            S['lad_exact_tests'] += 1
            if not true_ladder(X, p, n2, Cp, Tmax):
                S['lad_exact_fail'] += 1; print("FAIL ladder not exact on the event", p, X, n2)
    print(f"RESULT ladder rule p={p} cumulative {S}")
print(f"SUMMARY t4 {S}")
