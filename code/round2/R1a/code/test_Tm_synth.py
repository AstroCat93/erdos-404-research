# Synthetic test of Lemmas S_m / T_m for m >= 2 using 2-adic (integer) inputs e_0..e_{n-1} chosen so that
# levels 0..m-1 of the hierarchy stay integral; the last input e_n is binary.  The proofs of S_m/T_m use only
# integrality of the inputs, so they apply verbatim to this generalized process.
import random, sys
from fractions import Fraction as Fr
from hier_lib import v2i, vf
def hier_gen(y, inputs, jmax):
    u = [Fr(0)] * jmax
    for k, e in enumerate(inputs):
        n = k + 1; new = [Fr(0)] * jmax
        new[0] = (u[0] + e) / (y + n)
        for j in range(1, jmax): new[j] = (u[j] + new[j - 1]) / (y + n)
        u = new
    return u
def build(y, n, m, rnd, BIGE=1 << 120):
    inputs = []; u = [Fr(0)] * (m + 1)
    for k in range(n):
        d = v2i(y + k + 1)
        e = rnd.getrandbits(100)
        # adjust e level by level: want new u^(j) integral for j < m
        for j in range(m):
            for _ in range(200):
                new = hier_gen(y, inputs + [e], m + 1) if False else None
                break
        # direct solve: brute adjust e modulo 2^{(j+1)d} digit by digit
        for bit in range(m * d + 2):
            pass
        # simple search: e = e0 + t*1, choose t mod 2^{m d} to make levels integral
        best = None
        base = e - (e % (1 << (m * d))) if d else e
        for t in range(1 << (m * d)) if m * d <= 14 else []:
            cand = base + t
            uu = [Fr(0)] * (m + 1)
            uu[0] = (u[0] + cand) / (y + k + 1)
            ok = vf(uu[0]) >= 0
            for j in range(1, m + 1):
                uu[j] = (u[j] + uu[j - 1]) / (y + k + 1)
                if j < m and vf(uu[j]) < 0: ok = False
            if ok: best = (cand, uu); break
        if best is None: return None
        inputs.append(best[0]); u = best[1]
    return inputs, u
rnd = random.Random(int(sys.argv[1])); trials = int(sys.argv[2])
stats = {}; fails = 0; tested = 0
for t in range(trials):
    m = rnd.choice([2, 2, 3]); n = rnd.randrange(10, 24)
    y = rnd.getrandbits(90) & ~1
    r = build(y, n, m, rnd)
    if r is None: continue
    inputs, u = r
    P = sum(v2i(y + l) for l in range(1, n + 1)); M = max(v2i(y + l) for l in range(1, n + 1))
    pin = 1
    for l in range(1, n + 1): pin *= (y + l)
    lam = vf(m * u[m] * pin); sig = P - lam
    if not (sig >= lam + M + 1): stats['unstable'] = stats.get('unstable', 0) + 1; continue
    # S_m checks
    for _ in range(4):
        h1 = rnd.getrandbits(30) << sig; h2 = rnd.getrandbits(30) << sig
        a = hier_gen(y + h1, inputs, m); b = hier_gen(y + h2, inputs, m)
        if not all(vf(a[j]) >= 0 for j in range(m)): fails += 1; print("S_m flat FAIL")
        if h1 != h2 and vf(a[m - 1] - b[m - 1]) != v2i(h1 - h2) - sig: fails += 1; print("S_m iso FAIL", vf(a[m-1]-b[m-1]), v2i(h1-h2)-sig)
        for j in range(m - 1):
            if h1 != h2 and vf(a[j] - b[j]) < v2i(h1 - h2) - v2i(m): fails += 1; print("S_m low FAIL", j)
    d = v2i(y + n + 1)
    if d >= sig or d > 9 or not (sig >= (m - 1) * d + v2i(m) + 2): stats['bad_d'] = stats.get('bad_d', 0) + 1; continue
    res = {}
    for en in (0, 1):
        res[en] = []
        for j in range(1 << d):
            yy = y + (j << sig) + (rnd.getrandbits(40) << (sig + d))
            uu = hier_gen(yy, inputs + [en], m)
            if all(vf(uu[i]) >= 0 for i in range(m)): res[en].append(j)
    if d == 0: ok = all(len(res[en]) == 1 for en in (0, 1))
    else: ok = len([en for en in (0, 1) if res[en]]) <= 1 and all(len(res[en]) <= 1 for en in (0, 1))
    tested += 1; key = (m, min(d, 3)); stats[key] = stats.get(key, 0) + 1
    if not ok: fails += 1; print("T_m FAIL", m, d, sig, lam, M, {k: len(v) for k, v in res.items()})
print("stats", stats, "transition tests", tested, "failures", fails)
