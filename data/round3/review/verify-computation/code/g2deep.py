"""Referee: exact min(g_2(a), cap) for natural a by the normalised-state recursion (big integers).
Independent of T4's p2add.c / gsampleN.c and T2's gcap.py (none read).
For a path alive at length n (2^{V_n} | S), sigma = S/pi_n(a) mod 2^{cap-V_n}; child b in {0,1}:
t = sigma+b; value candidate V_n + v(t); alive iff v(t) >= j = v(a+n+1); sigma' = (t/2^j) * u^{-1}.
Usage: python3 g2deep.py cap a1 a2 ...    or   python3 g2deep.py range cap A   (all 1<=a<=A)"""
import sys, time

def v2(z):
    return (z & -z).bit_length() - 1

def g2(a, cap):
    V = 0
    cur = {0}
    first = True
    best = 0
    n = 0
    while True:
        xn = a + n + 1
        j = v2(xn)
        u = xn >> j
        mod = 1 << (cap - V)
        nxt = set()
        uinv = None
        for s in cur:
            for b in ((1,) if first else (0, 1)):
                t = (s + b) % mod
                vt = (cap - V) if t == 0 else v2(t)
                if V + vt >= cap:
                    return cap
                if V + vt > best:
                    best = V + vt
                if vt >= j:
                    if V + j >= cap:
                        return cap
                    mod2 = 1 << (cap - V - j)
                    if uinv is None:
                        uinv = pow(u, -1, mod2)
                    nxt.add(((t >> j) * uinv) % mod2)
        first = False
        if not nxt:
            return best
        V += j
        cur = nxt
        n += 1

def vfact2(a):
    return a - bin(a).count("1")

if __name__ == "__main__":
    if sys.argv[1] == "range":
        cap = int(sys.argv[2]); A = int(sys.argv[3])
        for a in range(1, A + 1):
            print(a, g2(a, cap))
    else:
        cap = int(sys.argv[1])
        for a in map(int, sys.argv[2:]):
            t0 = time.time()
            g = g2(a, cap)
            print(f"a={a} cap={cap} min(g2,cap)={g} {'(exact: below cap)' if g < cap else '(>= cap)'} "
                  f"f(a,2)={'%d' % (vfact2(a) + g) if g < cap else '>= %d' % (vfact2(a) + cap)} [{time.time() - t0:.1f}s]",
                  flush=True)
