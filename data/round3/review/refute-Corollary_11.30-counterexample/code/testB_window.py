# Test B: exact check of the window identities (11.4) (unweighted and rho-weighted),
# Prop 10.6(i) (child slope = parent slope), and constancy on the cylinder, on full
# cylinders C_n(x) = x + 2^{V_n} Z_2 (all w mod 2^D, two random high tails each).
import sys, random
from fractions import Fraction
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from lib import *

seed = int(sys.argv[1]); TRIALS = int(sys.argv[2]); Lsel = int(sys.argv[3]); DMAX = int(sys.argv[4])
rng = random.Random(seed)
CL = {1: (0, 3), 3: (2, 3), 6: (6, 4)}  # L -> class (r0,k) used in the note
r0, k = CL[Lsel]
L = Lsel
l0 = 2 * L + 2
done = 0; bad = []
tries = 0
while done < TRIALS and tries < 200 * TRIALS:
    tries += 1
    x = rand_in_class(r0, k, rng) if rng.random() < 0.7 else rand_in_class(rng.randrange(0, 1 << k, 2), k, rng)
    n = rng.randint(19, 40)
    N = n + l0
    m = Vn(x, n)
    MN = Mn(x, N)
    if not (2 * MN + 3 * L + 3 <= m):
        continue
    VN = Vn(x, N)
    D = VN - m
    if D > DMAX:
        continue
    pi, dpi = pis(x, N)
    par, V = alive_paths(x, n, pi, dpi)
    allpar = par
    par = [p for p in par if v(p[2]) <= L]
    if not allpar:
        continue
    # predicted sums over w (times 2^D): 2^D * 2^{W_N-W_n} rho_n(e)
    WN_Wn = (N - VN) - (n - m)
    pred = {}
    for e, S, dS in par:
        r, lam = rho(x, n, S, dS, pi[n], m)
        pred[e] = (Fraction(2) ** WN_Wn) * r * (1 << D)
    cnt = {e: 0 for e in pred}
    wsum = {e: Fraction(0) for e in pred}
    x0 = x % (1 << m)
    ok = True
    for w in range(1 << D):
        for tail in range(2):
            xp = (x0 + (w << m) + (rng.getrandbits(P) << (m + D))) & MASK
            pip, dpip = pis(xp, N)
            allN, VNp = alive_paths(xp, N, pip, dpip)
            if VNp[N] != VN or VNp[n] != m:
                bad.append(('V not constant', x, n)); ok = False
            parp, _ = alive_paths(xp, n, pip, dpip)
            if set(p[0] for p in parp) != set(p[0] for p in alive_paths(x, n, pi, dpi)[0]):
                bad.append(('parents not constant', x, n)); ok = False
            c_here = {}
            w_here = {}
            for e2, S2, dS2 in allN:
                pe = e2[:n]
                if pe not in pred:
                    if v(dS2) <= L:
                        bad.append(('child slope<=L but parent slope>L', x, n, e2))
                    continue
                parS = [p for p in parp if p[0] == pe][0]
                if v(dS2) != v(parS[2]):
                    bad.append(('child slope != parent slope', x, n, e2))
                r2, lam2 = rho(xp, N, S2, dS2, pip[N], VN)
                c_here[pe] = c_here.get(pe, 0) + 1
                w_here[pe] = w_here.get(pe, Fraction(0)) + r2
            if tail == 0:
                for pe in c_here:
                    cnt[pe] += c_here[pe]; wsum[pe] += w_here[pe]
                first = (c_here, w_here)
            else:
                if first != (c_here, w_here):
                    bad.append(('depends on bits beyond m+D', x, n, w))
    for e in pred:
        if cnt[e] != pred[e] or wsum[e] != pred[e]:
            bad.append(('identity fails', x % (1 << 40), n, e, cnt[e], wsum[e], pred[e]))
    done += 1
    print(f"trial {done}: n={n} m={m} D={D} M_N={MN} parents={len(par)} total_pred={sum(pred.values())} total_cnt={sum(cnt.values())} total_w={sum(wsum.values())}", flush=True)
print("L=%d trials=%d failures=%d" % (L, done, len(bad)))
for b in bad[:10]:
    print(b)
