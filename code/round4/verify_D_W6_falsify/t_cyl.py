"""Exact falsification tests of M4D Lemma W1, Lemma W2, Lemma W3, Proposition W4 and Corollary W5
on cylinders C = x + p^m Z_p (m = V_n(x)) with windows W = [n,N), W' = [N,N').

usage: python3 t_cyl.py p n H H2 seed ncyl kinds [psub] [kextra] [maxcombos]
  kinds: comma list of x-samplers: rand, gate_hist, gate_win, near2, tight, any (no D,D'>=1 filter)

Brute side (wf_core.Cyl): exact populations by direct evaluation at every point of C mod p^Ken.
Formula side: the statements' right-hand sides from the window sums Q_f(x).
Exact rationals throughout, except the per-frequency form of W3(b) (mpmath, 50 digits) and the
literal complex-exponential forms of W2 and W4 (float64, used only as a cross-check of the exact
Parseval forms).
"""
import sys, time, random
from fractions import Fraction
import numpy as np
import mpmath
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from wf_core import *

p, n, H, H2, seed, ncyl = [int(t) for t in sys.argv[1:7]]
kinds = sys.argv[7].split(',')
psub = int(sys.argv[8]) if len(sys.argv) > 8 and sys.argv[8] != '-' else None
kextra = int(sys.argv[9]) if len(sys.argv) > 9 else 0
maxcombos = int(sys.argv[10]) if len(sys.argv) > 10 else 10 ** 9
full_children = len(sys.argv) > 11 and sys.argv[11] == 'full'
rnd = random.Random(seed)
nrng = np.random.default_rng(seed)
N = n + H
N2 = N + H2
print(f"p={p} n={n} H={H} H2={H2} seed={seed} ncyl={ncyl} kinds={kinds} psub={psub} kextra={kextra} maxcombos={maxcombos} full_children={full_children}")

CHK = {}      # name -> [checks, failures]
FAILS = []    # (name, details)
MAXR = {}     # name -> max ratio
EQ = {}       # name -> count of exact equalities
MINR = {}
SKIPPED = {}


def chk(name, ok, detail=None):
    c = CHK.setdefault(name, [0, 0])
    c[0] += 1
    if not ok:
        c[1] += 1
        if len(FAILS) < 40:
            FAILS.append((name, detail))


def ratio(name, num, den):
    if den > 0:
        r = num / den
        if name not in MAXR or r > MAXR[name][0]:
            MAXR[name] = (r, None)


def unit(p, rnd):
    while True:
        u = rnd.randrange(1, p ** 6)
        if u % p:
            return u


def sample_x(kind):
    B = p ** 40
    if kind in ('rand', 'tight', 'any', 'D0', 'D20'):
        return rnd.randrange(B)
    if kind == 'gate_hist':
        i = rnd.randint(1, n)
        s = rnd.randint(2, 4)
        return (unit(p, rnd) * p ** s - i) % B
    if kind == 'gate_win':
        i = rnd.randint(n + 1, N2)
        s = rnd.randint(2, 3)
        return (unit(p, rnd) * p ** s - i) % B
    if kind == 'near2':
        s = rnd.randint(2, 5)
        return (unit(p, rnd) * p ** s - 2) % B
    raise ValueError(kind)


def accept(c, kind):
    if not c.ok or c.P == 0:
        return False
    if kind == 'any':
        return True
    if kind == 'D0':
        return c.D == 0
    if kind == 'D20':
        return c.D2 == 0
    if c.D < 1 or c.D2 < 1:
        return False
    if kind == 'tight':
        return c.D + c.D2 == c.m - c.M[N2]
    return True


# ---------------------------------------------------------------- weights
def parent_schemes(c):
    P = c.P
    out = {}
    out['ones'] = [1] * P
    out['rand'] = [0 if rnd.random() < 0.2 else rnd.randint(1, 50) for _ in range(P)]
    if sum(out['rand']) == 0:
        out['rand'][0] = 1
    s = [0] * P
    s[rnd.randrange(P)] = 1
    out['single'] = s
    # largest beta-class mod p^{D'}
    PD2 = p ** c.D2
    cls = {}
    for i, b in enumerate(c.beta):
        cls.setdefault(b % PD2, []).append(i)
    big = max(cls.values(), key=len)
    out['class'] = [1 if i in set(big) else 0 for i in range(P)]
    out['zero'] = [0] * P
    return out


def q_schemes(c):
    HH = 1 << H
    out = {}
    out['unif'] = Weight([1] * HH, 'unif')
    out['rand'] = Weight([rnd.randint(0, 1000) for _ in range(HH)] , 'rand')
    a = [0] * HH
    for f in rnd.sample(range(HH), 3):
        a[f] = rnd.randint(1, 10)
    out['sparse'] = Weight(a, 'sparse')
    a = [0] * HH
    a[rnd.randrange(HH)] = 1
    out['point'] = Weight(a, 'point')
    out['qstar'] = q_star(c.Q, p, c.D, c.D2)
    # uniform over the residues of Sigma mod p^K, split evenly among representatives
    PK = p ** c.K
    res = (c.Q % PK).tolist()
    cnt = {}
    for r in res:
        cnt[r] = cnt.get(r, 0) + 1
    out['resunif'] = Weight.from_fractions([Fraction(1, len(cnt) * cnt[r]) for r in res], 'resunif')
    # all mass on one class r0 mod p^D, uniform over its words
    PD = p ** c.D
    r0 = rnd.choice(res) % PD
    out['class1'] = Weight([1 if r % PD == r0 else 0 for r in res], 'class1')
    return out


def q2_schemes(c, wpar, q):
    """weights on W': constant on C (const=True) or varying with C' (const=False)"""
    H2H = 1 << H2
    nC = p ** c.D
    out = {}
    out['unif'] = (True, [Weight([1] * H2H)] * nC)
    w = Weight([rnd.randint(0, 1000) for _ in range(H2H)])
    out['rand'] = (True, [w] * nC)
    a = [0] * H2H
    a[rnd.randrange(H2H)] = 1
    out['point'] = (True, [Weight(a)] * nC)
    res = (c.Q2 % (p ** c.D2)).tolist()
    cnt = {}
    for r in res:
        cnt[r] = cnt.get(r, 0) + 1
    out['res'] = (True, [Weight.from_fractions([Fraction(1, len(cnt) * cnt[r]) for r in res])] * nC)
    out['vrand'] = (False, [Weight([rnd.randint(0, 1000) for _ in range(H2H)]) for _ in range(nC)])
    tab = []
    for _ in range(nC):
        a = [0] * H2H
        a[rnd.randrange(H2H)] = 1
        tab.append(Weight(a))
    out['vpoint'] = (False, tab)
    out['vmax'] = (False, vmax_table(c, wpar, q))
    return out


def vmax_table(c, wpar, q):
    """per C', the point mass on W' maximising Var_{C'}(M_N') (exact integer comparison)"""
    H2H = 1 << H2
    nC = p ** c.D
    nW = c.nW
    one = [Weight([1] + [0] * (H2H - 1))] * nC
    sN, sN2, prod = c.sums(wpar, q, one)
    mat = np.zeros((nW, H2H), dtype=object)
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


# ---------------------------------------------------------------- exact checks
def EC(vals):
    return sum(vals, Fraction(0)) / len(vals)


def check_W1(c, wpar, q, btab, tag):
    """exact W1(b), W1 step 1 (per C'), constancy of M_N on C'; returns integer sums and exact
    E_C[M_N'^2] - E_C[M_N^2] (the left side of W4) and Var_C(M_N)."""
    sN, sN2, prod = c.sums(wpar, q, btab)
    nC = p ** c.D
    nW = c.nW
    m, D, K = c.m, c.D, c.K
    W = sum(wpar)
    Mn = p ** m * W
    chk('W1b E_C[M_N]=M_n', p ** (m + D) * sum(sN) == nW * q.den * Mn, (tag,))
    okc = True
    okconst = True
    for cc in range(nC):
        ws = range(cc, nW, nC)
        v = sN[cc]
        if any(sN[w] != v for w in ws):
            okconst = False
        if p ** (K - D) * sum(sN2[w] for w in ws) != len(ws) * btab[cc].den * v:
            okc = False
    chk("W1 step1 E_C'[M_N']=M_N(C')", okc, tag)
    chk("M_N constant on C'", okconst, tag)
    EN2 = Fraction(p ** (2 * (m + D)) * sum(s * s for s in sN), nW * q.den ** 2)
    EN22 = sum((Fraction(sum(sN2[w] ** 2 for w in range(cc, nW, nC)), btab[cc].den ** 2) for cc in range(nC)),
               Fraction(0)) * Fraction(p ** (2 * (m + K)), nW * q.den ** 2)
    EN = Fraction(p ** (m + D) * sum(sN), nW * q.den)
    return sN, sN2, prod, EN22 - EN2, EN2 - EN ** 2, Mn


def W2_exact(c, wpar, q, sN, var, Mn, tag):
    """W2 identity in exact Parseval form + bound + pointwise child-mass identity"""
    PD = p ** c.D
    m = c.m
    hD = np.array(mu_hist(c.Q, q, p, c.D), dtype=object)
    warr = np.arange(c.nW, dtype=np.int64)
    z = np.zeros(c.nW, dtype=object)
    for e in range(c.P):
        if wpar[e]:
            idx = (c.tau0[e] % PD - (c.beta[e] % PD) * warr) % PD
            z = z + wpar[e] * hD[idx]
    chk('W2 pointwise child mass (Prop B(i) weighted)', all(int(z[w]) == sN[w] for w in range(c.nW)), tag)
    cr = [0] * PD
    QD = (c.Q % PD).tolist()
    for e in range(c.P):
        if not wpar[e]:
            continue
        b = c.beta[e] % PD
        binv = inv(b, p, c.D) if c.D > 0 else 0
        phi = (c.tau0[e] * binv) % PD
        for f, qf in enumerate(QD):
            if q.a[f]:
                cr[(phi - binv * qf) % PD] += wpar[e] * q.a[f]
    W = sum(wpar)
    rhs = Fraction(p ** (2 * m) * (PD * sum(t * t for t in cr) - (W * q.den) ** 2), q.den ** 2)
    chk('W2 identity (exact Parseval form)', var == rhs, (tag, var, rhs))
    bound = Fraction(Mn) ** 2 * chi2(c.Q, q, p, c.D)
    chk('W2 bound Var <= M_n^2 chi^2_q', var <= bound, (tag, var, bound))
    if bound > 0:
        ratio('W2 Var/bound', var, bound)
    if sum(1 for t in wpar if t) == 1:
        chk('W2 equality for a single parent', var == bound, (tag, var, bound))
    return var


def W2_literal(c, wpar, q, var):
    """literal complex form p^{2m} sum_{eta!=0} |sum_e w(e) muhat(eta beta_e^{-1}) e(eta phi_e/p^D)|^2"""
    PD = p ** c.D
    QD = (c.Q % PD)
    a = np.array(q.a, dtype=float) / q.den
    zeta = np.arange(PD)
    muhat = np.array([np.sum(a * np.exp(-2j * np.pi * z * QD / PD)) for z in zeta])
    A = np.zeros(PD, dtype=complex)
    for e in range(c.P):
        if not wpar[e]:
            continue
        b = c.beta[e] % PD
        binv = inv(b, p, c.D)
        phi = (c.tau0[e] * binv) % PD
        A += wpar[e] * muhat[(zeta * binv) % PD] * np.exp(2j * np.pi * zeta * phi / PD)
    val = p ** (2 * c.m) * np.sum(np.abs(A[1:]) ** 2)
    ok = abs(val - float(var)) <= 1e-9 * max(1.0, abs(float(var)))
    chk('W2 literal Fourier form (float)', ok, (float(var), val))


def W3_checks(c, wpar, q, prod, tag, control=False):
    """W3(a) exact; W3(b) summed over xi exact; W3(b) per xi in float64 (FFT), for every k <= k3"""
    m, D = c.m, c.D
    W = sum(wpar)
    if c.k3 < 1 or W == 0:
        return
    nW = c.nW
    for k in range(1, c.k3 + 1):
        Pk = p ** k
        if nW * Pk > 2 * 10 ** 6:
            SKIPPED['W3 level k skipped (table > 2e6 entries)'] = SKIPPED.get('W3 level k skipped (table > 2e6 entries)', 0) + 1
            continue
        cw = np.zeros((nW, Pk), dtype=object)
        if len(prod):
            np.add.at(cw, (c.ch_w, c.ch_tau % Pk), prod.astype(object))
        tot = [int(t) for t in cw.sum(axis=0)]
        if not control:
            chk('W3(a) E_C Psi(xi)=0 (child-target mass flat in s)', len(set(tot)) == 1, (tag, k, tot[:5]))
        rowsum = cw.sum(axis=1)
        L0 = int((cw * cw).sum())
        Lsum = int((rowsum * rowsum).sum())
        PDk = p ** (D + k)
        h = mu_hist(c.Q, q, p, D + k)
        ac0 = sum(t * t for t in h)
        hcls = [0] * (p ** D)
        for r, t in enumerate(h):
            hcls[r % p ** D] += t
        acsum = sum(t * t for t in hcls)        # = sum_{d'} ac(p^D d')
        u = c.u % Pk
        uinv = inv(u, p, k)
        if control:
            uinv = u  # NEGATIVE CONTROL: wrong unit in the fibre (zeta = xi*u instead of xi*u^{-1})
        lhs_sum = Fraction(p ** (2 * (m + D)) * (Pk * L0 - Lsum), nW * q.den ** 2)
        F_sum = Fraction(p ** D * (Pk * ac0 - acsum), q.den ** 2)
        if not control:
            et = eps_tilde(c.Q, q, p, D, k)
            chk('W3 identity sum_{xi!=0} F^q = eps~ (level k)', F_sum == et, (tag, k, F_sum, et))
            rhs_sum = Fraction(p ** m * W) ** 2 * F_sum
            chk('W3(b) summed over xi (exact)', lhs_sum <= rhs_sum, (tag, k, lhs_sum, rhs_sum))
            if rhs_sum > 0:
                ratio('W3(b) summed LHS/RHS', lhs_sum, rhs_sum)
            if sum(1 for t in wpar if t) == 1:
                chk('W3(b) summed: equality for a single parent', lhs_sum == rhs_sum, (tag, k))
        # per xi, float64: LHS_n(xi) = E_C|Psi(xi)|^2 p^{2(m+D)} / (p^m W)^2 ; F^q(xi)
        scale = float(max(1, max(abs(int(t)) for t in cw.ravel())))
        cwf = np.array(cw, dtype=float) / scale
        Fx = np.fft.fft(cwf, axis=1)
        lhs_xi = (np.abs(Fx) ** 2).sum(axis=0) * (scale ** 2) * float(p ** (2 * D)) / (nW * float(q.den) ** 2 * float(W) ** 2)
        hf = np.array(h, dtype=float) / q.den
        muh = np.fft.fft(hf)
        zeta = np.arange(PDk)
        for xi in range(1, Pk):
            F = float(np.sum(np.abs(muh[(zeta % Pk) == (xi * uinv) % Pk]) ** 2))
            name = 'W3(b) per xi (float64 FFT, rel. tol 1e-9)' if not control else 'NC3 W3(b) per xi with u instead of u^{-1}'
            chk(name, lhs_xi[xi] <= F + 1e-9 * max(1.0, F), (tag, k, xi, lhs_xi[xi], F))
            if not control and F > 1e-12:
                ratio('W3(b) per-xi LHS/RHS (float)', lhs_xi[xi], F)


def W4_checks(c, wpar, q, q2name, const, btab, LHS, Mn, tag):
    et = eps_tilde(c.Q, q, p, c.D, c.D2)
    RHS = et * Mn ** 2
    chk('W4 adapted: LHS <= eps~^q M_n^2', LHS <= RHS, (tag, LHS, RHS))
    if RHS > 0:
        ratio('W4 adapted LHS/RHS', LHS, RHS)
    chk('W4 LHS >= 0 (E_C Var_{C\'})', LHS >= 0, (tag, LHS))
    single = sum(1 for t in wpar if t) == 1
    if single and q2name in ('point', 'vpoint', 'vmax'):
        chk('W4 equality: single parent and point-mass q\'', LHS == RHS, (tag, LHS, RHS))
        EQ['W4 single+point equality'] = EQ.get('W4 single+point equality', 0) + (LHS == RHS)
    if const:
        es = eps_sharp(c.comp, q, btab[0], p, c.D, c.D2)
        chk('W4 sharp: LHS <= eps^{q,q\'} M_n^2', LHS <= es * Mn ** 2, (tag, LHS, es * Mn ** 2))
        chk('eps^{q,q\'} <= eps~^q', es <= et, (tag, es, et))
        if es * Mn ** 2 > 0:
            ratio('W4 sharp LHS/RHS', LHS, es * Mn ** 2)
        return LHS, et, es
    else:
        # NEGATIVE CONTROL NC2: sharp form evaluated with the C'_0 weight although q' varies with C'
        es0 = eps_sharp(c.comp, q, btab[0], p, c.D, c.D2)
        chk('NC2 sharp form with varying q\' (control, failures expected)', LHS <= es0 * Mn ** 2, (tag,))
        return LHS, et, None


def W4_sharp_literal(c, q, q2):
    """sum_{xi!=0} |muhat^{q'}_{D'}(xi)|^2 F^q(xi) in float vs the exact composite-collision form"""
    D, D2 = c.D, c.D2
    PK = p ** (D + D2)
    P2 = p ** D2
    a = np.array(q.a, dtype=float) / q.den
    b = np.array(q2.a, dtype=float) / q2.den
    QK = c.Q % PK
    Q2 = c.Q2 % P2
    zeta = np.arange(PK)
    muK = np.array([np.sum(a * np.exp(-2j * np.pi * z * QK / PK)) for z in zeta])
    mu2 = np.array([np.sum(b * np.exp(-2j * np.pi * xx * Q2 / P2)) for xx in range(P2)])
    u = c.u % P2
    uinv = inv(u, p, D2)
    tot = 0.0
    for xi in range(1, P2):
        F = np.sum(np.abs(muK[(zeta % P2) == (xi * uinv) % P2]) ** 2)
        tot += abs(mu2[xi]) ** 2 * F
    es = eps_sharp(c.comp, q, q2, p, D, D2)
    chk('W4 sharp: Fourier form = composite-collision form (float)', abs(tot - float(es)) <= 1e-9 * max(1, abs(float(es))),
        (tot, float(es)))


def W5_checks(c, qs, tag):
    mW, lift, nrep = m_W5(c.Q, p, c.D, c.D2)
    complete = any(L == p ** c.D2 for L in lift)
    chk('W5 m=0 iff a complete class exists', (mW == 0) == complete, tag)
    qst = qs['qstar']
    est = eps_tilde(c.Q, qst, p, c.D, c.D2)
    chk('W5(b) eps~^{q*} = m(W;D\')', est == mW, (tag, est, mW))
    for name, q in qs.items():
        e = eps_tilde(c.Q, q, p, c.D, c.D2)
        chk('W5(a) eps~^q >= m(W;D\')', e >= mW, (tag, name, e, mW))
    HH = 1 << H
    # all point masses
    for f in range(HH):
        a = [0] * HH
        a[f] = 1
        e = eps_tilde(c.Q, Weight(a), p, c.D, c.D2)
        chk('W5(a) eps~^q >= m (all point masses)', e >= mW, (tag, f))
    # random Dirichlet-like and perturbations of q*
    for t in range(10):
        a = [int(1000 * rnd.expovariate(1.0)) for _ in range(HH)]
        if sum(a) == 0:
            a[0] = 1
        e = eps_tilde(c.Q, Weight(a), p, c.D, c.D2)
        chk('W5(a) eps~^q >= m (random)', e >= mW, (tag,))
    L = 10 ** 6
    for t in range(10):
        a = [int(L * qst.a[i] // qst.den) + (rnd.randint(0, 3) if rnd.random() < 0.3 else 0) for i in range(HH)]
        if sum(a) == 0:
            continue
        e = eps_tilde(c.Q, Weight(a), p, c.D, c.D2)
        chk('W5(a) eps~^q >= m (perturbed q*)', e >= mW, (tag,))
    # adversarial: projected-gradient minimisation of eps~ (float), evaluated exactly at the end
    PK = p ** c.K
    PD = p ** c.D
    QK = (c.Q % PK)
    QD = (c.Q % PD)
    best = None
    for start in range(3):
        x = np.array([rnd.random() for _ in range(HH)])
        x /= x.sum()
        for it in range(400):
            hK = np.bincount(QK, weights=x, minlength=PK)
            hD = np.bincount(QD, weights=x, minlength=PD)
            g = 2 * (PK * hK[QK] - PD * hD[QD])
            x = x - 0.5 / PK * g
            # projection onto simplex
            u_ = np.sort(x)[::-1]
            css = np.cumsum(u_)
            rho = np.nonzero(u_ * np.arange(1, HH + 1) > (css - 1))[0][-1]
            th = (css[rho] - 1) / (rho + 1.0)
            x = np.maximum(x - th, 0)
        a = [int(round(t * 10 ** 9)) for t in x]
        if sum(a) == 0:
            continue
        e = eps_tilde(c.Q, Weight(a), p, c.D, c.D2)
        chk('W5(a) eps~^q >= m (gradient-descent minimiser)', e >= mW, (tag, float(e), float(mW)))
        if best is None or e < best:
            best = e
    if best is not None and mW > 0:
        r = best / mW
        if 'W5 min over descent of eps~/m (>=1 expected)' not in MINR or r < MINR['W5 min over descent of eps~/m (>=1 expected)']:
            MINR['W5 min over descent of eps~/m (>=1 expected)'] = r
    if best is not None and mW == 0:
        EQ['W5 descent reached eps~=0 when m=0'] = EQ.get('W5 descent reached eps~=0 when m=0', 0) + (best == 0)
    return mW, complete


# ---------------------------------------------------------------- main loop
t0 = time.time()
ncyl_done = 0
attempts = 0
info_rows = []
cyl_kinds = {}
quota = {k: (ncyl + len(kinds) - 1) // len(kinds) for k in kinds}
tries = {k: 0 for k in kinds}
while ncyl_done < ncyl:
    open_kinds = [k for k in kinds if cyl_kinds.get(k, 0) < quota[k] and tries[k] < 3000]
    if not open_kinds:
        break
    kind = open_kinds[attempts % len(open_kinds)]
    attempts += 1
    tries[kind] += 1
    x = sample_x(kind)
    v, V, M = valdata(x, p, N2)
    m = V[n]
    D = V[N] - m
    D2 = V[N2] - V[N]
    if not ((D + D2 <= m - M[N2]) and (M[N2] < m)):
        continue
    if kind == 'D0' and D != 0:
        continue
    if kind == 'D20' and D2 != 0:
        continue
    if kind not in ('any', 'D0', 'D20') and (D < 1 or D2 < 1):
        continue
    if kind == 'tight' and D + D2 != m - M[N2]:
        continue
    # resource guards (not part of any claim): keep the enumeration Z/p^Ken below 3^9 points and the working
    # modulus p^(m+Ken+1) below 2^56 (int64 arithmetic)
    M_N = M[N]
    kx = kextra
    while kx > 0 and p ** (D + min(D2 + kx, m - M_N - D)) > 3 ** 9:
        kx -= 1
    Ken_est = max(D + D2, D + (min(D2 + kx, m - M_N - D) if kx > 0 else D2))
    if p ** (m + Ken_est + 1) >= 2 ** 56 or p ** Ken_est > 3 ** 9:
        SKIPPED['resource guard'] = SKIPPED.get('resource guard', 0) + 1
        continue
    c = Cyl(p, x, n, H, H2, kextra=kx, rng=nrng, psub=psub, full_children=full_children)
    if not accept(c, kind):
        continue
    ncyl_done += 1
    cyl_kinds[kind] = cyl_kinds.get(kind, 0) + 1
    tag0 = (kind, x % p ** (c.m + c.Ken), c.m, c.D, c.D2)
    st = c.stats
    chk('W1(a) children of slope-0 parents have slope 0', st['w1a_child_slope_bad'] == 0, (tag0, st))
    chk('W1(a) children of slope>0 parents have slope>0', st['w1a_hi_child_slope0'] == 0, (tag0, st))
    chk('W1(a) grandchildren: slope 0 iff line slope 0', st['w1a_gchild_bad'] == 0, (tag0, st))
    chk('Lemma 2(a) parents alive/slope constant on C', st['parent_const_bad'] == 0, (tag0, st))
    chk('Lemma 2(a) alive set at n identical at sampled x\' (BFS)', st['parent_set_bad'] == 0, (tag0, st))
    chk('locality: alive structure at N, N\' depends on w mod p^Ken only', st['locality_bad'] == 0 and st['locality_checked'] > 0, (tag0, st))
    PW = parent_schemes(c)
    QS = q_schemes(c)
    mW, complete = W5_checks(c, QS, tag0)
    info_rows.append((kind, c.m, c.D, c.D2, c.M[N2], c.nalive_all, c.P0_all, c.P, len(c.gc_w), float(mW), complete))
    combos = []
    for pwn in PW:
        for qn in QS:
            combos.append((pwn, qn))
    if len(combos) > maxcombos:
        keep = [cb for cb in combos if cb[0] in ('single',) or cb[1] in ('qstar',)]
        rest = [cb for cb in combos if cb not in keep]
        rnd.shuffle(rest)
        combos = keep + rest[:max(0, maxcombos - len(keep))]
    for (pwn, qn) in combos:
        wpar = PW[pwn]
        q = QS[qn]
        Q2S = q2_schemes(c, wpar, q)
        var = None
        for q2n, (const, btab) in Q2S.items():
            tag = tag0 + (pwn, qn, q2n)
            sN, sN2, prod, LHS, varN, Mn = check_W1(c, wpar, q, btab, tag)
            if var is None:
                var = W2_exact(c, wpar, q, sN, varN, Mn, tag)
                if rnd.random() < 0.3 and c.D >= 1 and sum(wpar):
                    W2_literal(c, wpar, q, var)
                if sum(wpar):
                    W3_checks(c, wpar, q, prod, tag)
                    if rnd.random() < 0.25:
                        W3_checks(c, wpar, q, prod, tag, control=True)
            _, et, es = W4_checks(c, wpar, q, q2n, const, btab, LHS, Mn, tag)
            if const and rnd.random() < 0.15 and c.D2 >= 1:
                W4_sharp_literal(c, q, btab[0])
            nC = p ** c.D
            nonconst = any(len(set(sN2[w] for w in range(cc, c.nW, nC))) > 1 for cc in range(nC))
            # W5(c): complete coset + q*  =>  M_N' constant on every C' (any q', any parent weights)
            if complete and qn == 'qstar':
                chk('W5(c) complete coset + q*: M_N\' constant on every C\'', not nonconst, tag)
                chk('W5(c) complete coset + q*: LHS = 0', LHS == 0, (tag, LHS))
            if complete and qn in ('unif', 'rand') and pwn in ('ones', 'rand') and q2n in ('unif', 'rand', 'vrand'):
                nm = 'control: complete coset, q in {unif, rand}: count of cases with M_N\' constant on every C\''
                CHK.setdefault(nm, [0, 0])
                CHK[nm][0] += 1
                if not nonconst:
                    CHK[nm][1] += 1
    # NEGATIVE CONTROL NC1: q varying inside C (with C') breaks the martingale identity W1(b)
    wpar = PW['ones']
    nC = p ** c.D
    if nC > 1:
        qtab = [Weight([rnd.randint(0, 1000) for _ in range(1 << H)]) for _ in range(nC)]
        tot = Fraction(0)
        for cc in range(nC):
            sN, _, _ = c.sums(wpar, qtab[cc], [Weight([1] * (1 << H2))] * nC)
            tot += sum(Fraction(p ** (c.m + c.D) * sN[w], qtab[cc].den) for w in range(c.nW) if w % nC == cc)
        chk('NC1 q varying with C\' inside C: E_C[M_N]=M_n (control, failures expected)',
            tot / c.nW == p ** c.m * sum(wpar), (tag0,))
    # NEGATIVE CONTROL NC4: drop the top shell of eps~ (use level K-1) in the single-parent equality case
    if c.D2 >= 1:
        wpar = PW['single']
        q = QS['rand']
        btab = q2_schemes(c, wpar, q)['vpoint'][1]
        _, _, _, LHS, _, Mn = check_W1(c, wpar, q, btab, tag0 + ('NC4',))
        wrong = eps_tilde(c.Q, q, p, c.D, c.D2 - 1) * Mn ** 2
        chk('NC4 W4 with eps~ at level K-1 (control, failures expected)', LHS <= wrong, (tag0,))

print("cylinders:", ncyl_done, "attempts:", attempts, "kinds:", cyl_kinds, "skipped:", SKIPPED)
print("cylinder table (kind, m, D, D', M_N', #alive_all, #P0_all, #P lines, #grandchildren total, m(W;D'), complete):")
for r in info_rows:
    print("  ", r)
print("checks:")
nfail_core = 0
for name in sorted(CHK):
    cnum, fnum = CHK[name]
    ctl = name.startswith('NC') or name.startswith('control')
    print(f"  {'[control] ' if ctl else ''}{name}: checks {cnum} failures {fnum}")
    if not ctl:
        nfail_core += fnum
print("max ratios:")
for name, (r, _) in sorted(MAXR.items()):
    print(f"  {name}: {float(r):.6g}" + (f"  (exact {r})" if isinstance(r, Fraction) and r == 1 else ""))
print("min ratios:", {k: float(v) for k, v in MINR.items()})
print("exact equalities:", EQ)
core_fails = [f for f in FAILS if not (f[0].startswith('NC') or f[0].startswith('control'))]
for f in core_fails[:10]:
    print("FAIL", f)
ctl_fails = [f for f in FAILS if f[0].startswith('NC')]
for f in ctl_fails[:3]:
    print("control failure example", f[0], f[1])
print(f"RESULT {'OK' if nfail_core == 0 else 'FAIL'} core_failures={nfail_core} time={time.time() - t0:.1f}s")
