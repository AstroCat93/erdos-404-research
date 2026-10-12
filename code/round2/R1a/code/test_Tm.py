# Exact test of Lemmas S_m / T_m (m = 1,2,3,...): see hier_lib.py for the hierarchy.
# m-flat at n: u0..u(m-1) in Z_2.  lambda = v(m*um_n*pi_n), sigma = P_n - lambda.  m-stable: sigma >= lambda+M+1.
# Checks (on the ball U = y + 2^sigma Z_2):
#  S_m: random points of U are m-flat; v(u(m-1)(y')-u(m-1)(y'')) = v(y'-y'') - sigma.
#  T_m: m=1: each e_n has exactly one valid class mod 2^(sigma+d) (d<sigma).
#       m>=2, d=0: both e_n, all classes;  d>=1 good (sigma >= (m-1)d+v(m)+2): <=1 e_n nonempty, <=1 class.
import random, sys
from hier_lib import *
def run(seed, trials, near2_frac=0.7, nlo=6, nhi=26):
    rnd = random.Random(seed)
    stats = {}; fails = 0
    for t in range(trials):
        if rnd.random() < near2_frac:
            w = rnd.randrange(2, 9); y = (1 << 90) - 2 + ((rnd.getrandbits(70) | 1) << w)
        else:
            y = rnd.getrandbits(90) & ~1
        n = rnd.randrange(nlo, nhi)
        for p in valid_paths(y, n, cap=50):
            u = hier(y, p); m = flat_order(u)
            if m == 0 or m >= JMAX - 1: continue
            P, M, pin = env(y, n)
            lam = vf(m * u[m] * pin); sig = P - lam
            if not (sig >= lam + M + 1): continue
            # S_m checks
            for _ in range(3):
                h1 = (rnd.getrandbits(30) << sig); h2 = (rnd.getrandbits(30) << sig)
                y1, y2 = y + h1, y + h2
                if not mflat(y1, p, m): fails += 1; print("S_m flat FAIL", m)
                if h1 != h2:
                    a = hier(y1, p, m)[m - 1]; b = hier(y2, p, m)[m - 1]
                    if vf(a - b) != v2i(h1 - h2) - sig: fails += 1; print("S_m isometry FAIL", m, vf(a - b), v2i(h1 - h2) - sig)
            d = v2i(y + n + 1)
            if d >= sig or d > 9: continue
            vm = v2i(m)
            if m >= 2 and not (sig >= (m - 1) * d + vm + 2): continue
            key = (m, min(d, 3)); stats[key] = stats.get(key, 0) + 1
            res = {}
            for en in (0, 1):
                res[en] = [j for j in range(1 << d)
                           if mflat(y + (j << sig) + (rnd.getrandbits(40) << (sig + d)), p + (en,), m)]
            if m == 1 or d == 0:
                ok = all(len(res[en]) == (1 << d if (m >= 2 and d == 0) else 1) for en in (0, 1))
            else:
                ok = len([en for en in (0, 1) if res[en]]) <= 1 and all(len(res[en]) <= 1 for en in (0, 1))
            if not ok:
                fails += 1; print("T_m FAIL m", m, "d", d, "sig", sig, "lam", lam, "M", M, {k: len(v) for k, v in res.items()})
    return stats, fails
if __name__ == "__main__":
    st, f = run(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]) if len(sys.argv) > 3 else 0.7)
    print("tested (m, min(d,3)) counts:", dict(sorted(st.items())), "failures", f)
