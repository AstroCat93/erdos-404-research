"""Adversarial search for counterexamples to W2's bound, W4 (adapted and sharp forms) and W5(a):
hill-climbing on integer parent weights w(e) >= 0 and window weights q, q' (exact rational objective).

usage: python3 t_adv.py p n H H2 seed ncyl iters [psub]

Objectives (each must stay <= 1 if the claims hold; equality is attained by a single parent):
  r_W2   = Var_C(M_N) / (M_n^2 chi^2_q)
  r_W4a  = (E_C M_N'^2 - E_C M_N^2) / (eps~^q M_n^2),  q' = per-C' variance-maximising point masses
  r_W4s  = (E_C M_N'^2 - E_C M_N^2) / (eps^{q,q'} M_n^2),  q' constant on C (searched as well)
  r_W5   = m(W;D') / eps~^q  (must be <= 1)
The search starts from >= 2 parents with positive weight in different beta-classes or with different
roots when possible, so that it probes the Cauchy-Schwarz / Minkowski steps rather than the trivial
single-parent equality.
"""
import sys, time, random
from fractions import Fraction
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from wf_core import *

p, n, H, H2, seed, ncyl, iters = [int(t) for t in sys.argv[1:8]]
psub = int(sys.argv[8]) if len(sys.argv) > 8 else None
rnd = random.Random(seed)
nrng = np.random.default_rng(seed)
N = n + H
N2 = N + H2
print(f"p={p} n={n} H={H} H2={H2} seed={seed} ncyl={ncyl} iters={iters} psub={psub}")


def lhs_parts(c, wpar, q, btab):
    sN, sN2, prod = c.sums(wpar, q, btab)
    nC = p ** c.D
    nW = c.nW
    m, D, K = c.m, c.D, c.K
    EN2 = Fraction(p ** (2 * (m + D)) * sum(s * s for s in sN), nW * q.den ** 2)
    EN22 = sum((Fraction(sum(sN2[w] ** 2 for w in range(cc, nW, nC)), btab[cc].den ** 2) for cc in range(nC)),
               Fraction(0)) * Fraction(p ** (2 * (m + K)), nW * q.den ** 2)
    EN = Fraction(p ** (m + D) * sum(sN), nW * q.den)
    return EN22 - EN2, EN2 - EN ** 2, sN, sN2, prod


def vmax(c, wpar, q):
    H2H = 1 << H2
    nC = p ** c.D
    one = [Weight([1] + [0] * (H2H - 1))] * nC
    sN, sN2, prod = c.sums(wpar, q, one)
    mat = np.zeros((c.nW, H2H), dtype=object)
    if len(c.gc_c):
        np.add.at(mat, (c.gc_w, c.gc_f), prod[c.gc_c].astype(object))
    tab = []
    for cc in range(nC):
        sub = mat[cc::nC]
        var = sub.shape[0] * (sub * sub).sum(axis=0) - sub.sum(axis=0) ** 2
        bf = int(np.argmax(np.array([int(t) for t in var], dtype=object)))
        a = [0] * H2H
        a[bf] = 1
        tab.append(Weight(a))
    return tab


def objectives(c, wpar, q, q2c):
    Mn = p ** c.m * sum(wpar)
    if Mn == 0:
        return None
    out = {}
    chi = chi2(c.Q, q, p, c.D)
    et = eps_tilde(c.Q, q, p, c.D, c.D2)
    nC = p ** c.D
    tab = vmax(c, wpar, q)
    LHSa, var, _, _, _ = lhs_parts(c, wpar, q, tab)
    out['r_W2'] = var / (Mn ** 2 * chi) if chi > 0 else None
    out['r_W4a'] = LHSa / (et * Mn ** 2) if et > 0 else (None if LHSa == 0 else Fraction(10 ** 9))
    LHSs, _, _, _, _ = lhs_parts(c, wpar, q, [q2c] * nC)
    es = eps_sharp(c.comp, q, q2c, p, c.D, c.D2)
    out['r_W4s'] = LHSs / (es * Mn ** 2) if es > 0 else (None if LHSs == 0 else Fraction(10 ** 9))
    mW, _, _ = m_W5(c.Q, p, c.D, c.D2)
    out['r_W5'] = mW / et if et > 0 else (None if mW == 0 else Fraction(10 ** 9))
    return out


best_all = {}
SH = []
viol = []
t0 = time.time()
done = 0
att = 0
while done < ncyl and att < 5000:
    att += 1
    x = rnd.randrange(p ** 40)
    v, V, M = valdata(x, p, N2)
    m = V[n]
    D = V[N] - m
    D2 = V[N2] - V[N]
    if not (D + D2 <= m - M[N2] and M[N2] < m and D >= 1 and D2 >= 1):
        continue
    c = Cyl(p, x, n, H, H2, rng=nrng, psub=psub)
    if not c.ok or c.P < 2:
        continue
    done += 1
    # wording check (logic-check fix F2): the sharp mass eps^{q,q'} can lie below m(W;D')
    mW, _, _ = m_W5(c.Q, p, c.D, c.D2)
    res2 = (c.Q2 % p ** c.D2).tolist()
    cnt = {}
    for r in res2:
        cnt[r] = cnt.get(r, 0) + 1
    covers = len(cnt) == p ** c.D2
    q2res = Weight.from_fractions([Fraction(1, len(cnt) * cnt[r]) for r in res2])
    qs = q_star(c.Q, p, c.D, c.D2)
    es_res = eps_sharp(c.comp, qs, q2res, p, c.D, c.D2)
    SH.append((covers, float(mW), float(es_res), es_res < mW))
    HH = 1 << H
    H2H = 1 << H2
    for obj in ('r_W2', 'r_W4a', 'r_W4s', 'r_W5'):
        # start: two or three parents, random q, random q'
        k = min(c.P, rnd.choice([2, 3]))
        wpar = [0] * c.P
        for e in rnd.sample(range(c.P), k):
            wpar[e] = rnd.randint(1, 20)
        qa = [rnd.randint(0, 20) for _ in range(HH)]
        if sum(qa) == 0:
            qa[0] = 1
        q2a = [rnd.randint(0, 20) for _ in range(H2H)]
        if sum(q2a) == 0:
            q2a[0] = 1
        cur = objectives(c, wpar, Weight(qa), Weight(q2a))
        curv = cur[obj] if cur and cur[obj] is not None else Fraction(-1)
        for it in range(iters):
            w2, qa2, q2a2 = list(wpar), list(qa), list(q2a)
            mv = rnd.random()
            if mv < 0.3 and obj != 'r_W5':
                e = rnd.randrange(c.P)
                w2[e] = max(0, w2[e] + rnd.choice([-3, -1, 1, 3, 10]))
                if sum(1 for t in w2 if t) < 2:
                    continue
            elif mv < 0.8:
                f = rnd.randrange(HH)
                qa2[f] = max(0, qa2[f] + rnd.choice([-5, -1, 1, 5, 20]))
                if sum(qa2) == 0:
                    continue
            else:
                f = rnd.randrange(H2H)
                q2a2[f] = max(0, q2a2[f] + rnd.choice([-5, -1, 1, 5, 20]))
                if sum(q2a2) == 0:
                    continue
            res = objectives(c, w2, Weight(qa2), Weight(q2a2))
            if res is None or res[obj] is None:
                continue
            if res[obj] >= curv:
                wpar, qa, q2a, curv = w2, qa2, q2a2, res[obj]
        npos = sum(1 for t in wpar if t)
        key = obj
        if key not in best_all or curv > best_all[key][0]:
            best_all[key] = (curv, npos, (x % p ** (c.m + c.K), c.m, c.D, c.D2))
        if curv > 1:
            viol.append((obj, curv, x, wpar, qa, q2a))
        print(f"  cyl x mod p^(m+K)={x % p ** (c.m + c.K)} m={c.m} D={c.D} D'={c.D2} P={c.P} {obj}: best {float(curv):.6f}"
              f" (exact {curv if curv == 1 else ''}) with {npos} weighted parents", flush=True)
print("best per objective (value, #weighted parents, cylinder):")
for k, v_ in best_all.items():
    print(f"  {k}: {float(v_[0]):.8f}  parents={v_[1]}  cyl={v_[2]}")
print("sharp mass vs m(W;D'): (W' covers Z/p^D', m, eps^{q*,q'_res}, eps < m):")
for r in SH:
    print("  ", r)
print("cylinders with eps^{q*,q'_res} < m(W;D'):", sum(1 for r in SH if r[3]), "of", len(SH),
      "; with W' covering Z/p^{D'}:", sum(1 for r in SH if r[0]))
print("violations (> 1):", len(viol))
for vv in viol[:5]:
    print("  VIOLATION", vv[:3])
print(f"RESULT {'OK' if not viol else 'FAIL'} violations={len(viol)} time={time.time() - t0:.1f}s")
