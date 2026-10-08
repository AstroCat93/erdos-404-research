#!/usr/bin/env python3
"""Drive exact window checks to push the 'full coverage frontier' of a tail set E_{N0}.

Claim maintained (proved by the exact checks):  E_{N0} mod p^{e(R)} = p^{e(N0)} Z / p^{e(R)} Z,
i.e. every class of p^{e(N0)}Z mod p^{e(R)} is a sum of distinct n!, N0 <= n < R.
Step: for the next block boundary G (multiple of p), find A <= R (A >= N0, multiple of p) such that
COVER(A, G) holds (checked by ./wincheck, exact).  Then the claim holds with R := G.

usage: frontier.py p N0 Gmax step tailmax maxwin [logfile]
"""
import subprocess, sys, os, time

FBLEVEL = 99
HERE = os.path.dirname(os.path.abspath(__file__))
WC = os.path.join(HERE, 'wincheck')
WC2 = os.path.join(HERE, 'wincheck2')

def vp(n, p):
    v = 0
    while n % p == 0:
        n //= p; v += 1
    return v

def main():
    p, N0, Gmax, step, tailmax, maxwin = map(int, sys.argv[1:7])
    log = open(sys.argv[7], 'a') if len(sys.argv) > 7 else None
    R0 = int(sys.argv[8]) if len(sys.argv) > 8 and int(sys.argv[8]) > 0 else None
    T2 = int(sys.argv[9]) if len(sys.argv) > 9 else tailmax
    global FBLEVEL
    FBLEVEL = int(sys.argv[10]) if len(sys.argv) > 10 else 99
    V = [0] * (Gmax + 2)
    for n in range(1, Gmax + 2):
        V[n] = V[n - 1] + vp(n, p)
    R = N0 if R0 is None else R0
    t0 = time.time()
    KM = int(125 * 0.6931471805599453 / __import__('math').log(p)) + 1
    MODK = p ** KM
    Uc = [1] * (Gmax + 2)   # unit part of n! mod p^KM
    for n in range(1, Gmax + 2):
        m = n
        while m % p == 0: m //= p
        Uc[n] = Uc[n - 1] * m % MODK
    def out(s):
        print(s, flush=True)
        if log: log.write(s + '\n'); log.flush()
    out(f"# p={p} N0={N0} e(N0)={V[N0]} Gmax={Gmax} step={step} tailmax={tailmax} maxwin={maxwin}")
    import math
    lp, l2 = math.log(p), math.log(2)
    learned = {}
    while R + p <= Gmax:
        G = R + p
        if vp(G, p) == 1:
            # single block [G-p, G): p elements of equal valuation with nonzero unit parts mod p;
            # Cauchy-Davenport => their subset sums cover Z/p, and the jump is v_p(G) = 1.
            R = G
            continue
        ok = False
        tried = 0
        cands = [A for A in range(R, N0 - 1, -p) if G - A <= maxwin and (G - A) * l2 >= (V[G] - V[A]) * lp
                 and (V[G] - V[A]) * lp < 125 * l2]
        rich = [A for A in cands if (G - A) * l2 - (V[G] - V[A]) * lp >= 5 * l2]
        poor = [A for A in cands if A not in rich]
        plist = [(tailmax, 300000), (tailmax, 5000000), (tailmax + 1, 5000000)]
        lv = vp(G, p)
        if lv in learned: plist = [learned[lv]] + [q for q in plist if q != learned[lv]]
        if lv >= FBLEVEL: plist = []   # deep gates: go straight to the split (wincheck2) method
        for (tm, hmax) in plist:
            env = dict(os.environ); env['HMAX'] = str(hmax)
            for A in rich + poor:
                tried += 1
                jump = V[G] - V[A]
                r = subprocess.run([WC, str(p), str(A), str(G), str(step), str(tm), str(Uc[A] % p ** (V[G] - V[A]))], capture_output=True, text=True, env=env)
                res = [l for l in r.stdout.splitlines() if l.startswith('RESULT')]
                if res and 'HOLDS' in res[0]:
                    ok = True
                    learned[lv] = (tm, hmax)
                    if vp(G, p) >= 3 or jump > 8:
                        out(f"G={G} v_p(G)={vp(G,p)} e(G)={V[G]}: COVER({A},{G}) holds (window {G-A}, jump {jump}, tries {tried}, tail {tm}, hmax {hmax})  [{time.time()-t0:.0f}s]")
                    break
            if ok: break
        if not ok:
            # fallback: one split A < M < G, W2=[M,G) exact bitset (e(G)-e(M) <= T2), W1=[A,M) enumerated
            M0 = G - p
            while M0 - p >= N0 and V[G] - V[M0 - p] <= T2:
                M0 -= p
            pairs = []
            for M in (M0, M0 + p, M0 + 2 * p):
                if M >= G: continue
                for kk in range(3, 40):
                    A = M - kk * p
                    if A < N0: break
                    if A > R or M - A > 30: continue
                    pairs.append((A, M))
            pairs.sort(key=lambda am: (am[1] - am[0]))
            for (A, M) in pairs:
                tried += 1
                r = subprocess.run([WC2, str(p), str(A), str(M), str(G), str(Uc[A] % p ** (V[G] - V[A])), '128'], capture_output=True, text=True)
                res = [l for l in r.stdout.splitlines() if l.startswith('RESULT')]
                if res and 'HOLDS' in res[0]:
                    ok = True
                    out(f"G={G} v_p(G)={vp(G,p)} e(G)={V[G]}: COVER({A},{G}) holds via split M={M} (window {G-A}, jump {V[G]-V[A]}, W2 exponent {V[G]-V[M]}) [wincheck2]  [{time.time()-t0:.0f}s]")
                    break
        if not ok:
            out(f"STOP at G={G} v_p(G)={vp(G,p)} e(G)={V[G]}: no covering window found among {tried} candidates (maxwin={maxwin})")
            break
        R = G
    out(f"FRONTIER p={p} N0={N0}: E_N0 covers p^{V[N0]}Z/p^{V[R]}Z  (R={R}, e(R)={V[R]})")

if __name__ == '__main__':
    main()
