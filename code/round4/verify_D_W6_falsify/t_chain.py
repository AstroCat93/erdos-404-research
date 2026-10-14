"""Finite-horizon exact test of M4D Theorem W6 (weighted conditional positive measure) along a chain of
windows W_l = [n_l, n_{l+1}), n_l = n0 + l*H, l = 0..L, on an admissible atom A of G_0 (j = 0).

usage: python3 t_chain.py p n0 H L seed natoms schedules ebar_modes [psub] [kinds]
  schedules: comma list of U (uniform, predictable), R (random, adapted), RP (random, predictable),
             S (q* of Cor W5 for (W_l; D_{l+1}) on the regime event R_{l+1}, uniform off it; adapted),
             P (random point masses, adapted), M (random mixtures of 2 point masses and uniform, adapted)
  ebar_modes: comma list of inf (no eps-stopping), med (ebar_l = median of eps over active atoms),
              q1 (lower quartile), tiny (ebar = 0: stop as soon as eps > 0)
  psub: if given, w_0 = indicator of a random subset of psub slope-0 parents (the lemmas allow any
        w >= 0; W6 itself has w_0 = 1, which is the default).

The whole atom A is enumerated exactly: every G_l-atom below A (cylinders x + p^{m_l} Z_p) is visited
while the process is not stopped; stopped atoms carry their frozen value.  Populations are computed by
direct evaluation of S_e at a representative of each atom (brute force), and re-checked at a second
random representative of sampled atoms (measurability).  Everything is exact (Fractions) except the
final Paley-Zygmund comparison, which involves square roots (mpmath, 50 digits).
"""
import sys, time, random, hashlib
from fractions import Fraction
import numpy as np
import mpmath
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from wf_core import *

mpmath.mp.dps = 50
p, n0, H, L, seed, natoms = [int(t) for t in sys.argv[1:7]]
schedules = sys.argv[7].split(',')
ebar_modes = sys.argv[8].split(',')
psub = int(sys.argv[9]) if len(sys.argv) > 9 and sys.argv[9] != '-' else None
kinds = sys.argv[10].split(',') if len(sys.argv) > 10 else ['rand']
rnd = random.Random(seed)
times = [n0 + l * H for l in range(L + 3)]   # n_0 .. n_{L+2}
NMAX = times[-1]
Rcap = 1
while p ** (Rcap + 1) * 64 * NMAX < 2 ** 62:
    Rcap += 1
print(f"p={p} times={times} L={L} seed={seed} natoms={natoms} schedules={schedules} ebar={ebar_modes} psub={psub} kinds={kinds} Rcap={Rcap}")

CHK = {}
FAILS = []
STATS = {}


def chk(name, ok, detail=None):
    c = CHK.setdefault(name, [0, 0])
    c[0] += 1
    if not ok:
        c[1] += 1
        if len(FAILS) < 30:
            FAILS.append((name, detail))


def hseed(*args):
    return int(hashlib.sha256(repr(args).encode()).hexdigest()[:16], 16)


FH = digits(H)


def window_sums(x, n, Hh, mod):
    """Q_f(x) = sum_i f_i prod_{s<=i}(x+n+s) mod `mod`, for all f (window [n, n+Hh))"""
    y = [1]
    for i in range(1, Hh):
        y.append(y[-1] * (x + n + i))
    ym = np.array([t % mod for t in y], dtype=object)
    return np.array([int(sum(ym[i] for i in range(Hh) if (fi >> i) & 1)) % mod for fi in range(1 << Hh)], dtype=np.int64)


def choose_q(sched, l, xC, mC, xParent, mParent, regime_next, Dl, Dnext):
    """q_l on W_l for the G_l-atom with representative xC (level mC)."""
    HH = 1 << H
    if sched == 'U':
        return Weight([1] * HH, 'U')
    if sched in ('R', 'RP', 'P', 'M'):
        if sched == 'RP':
            key = (sched, l, xParent % p ** mParent if mParent is not None else -1)
        else:
            key = (sched, l, xC % p ** mC)
        r = random.Random(hseed(seed, key))
        if sched in ('R', 'RP'):
            return Weight([r.randint(1, 1000) for _ in range(HH)], sched)
        if sched == 'P':
            a = [0] * HH
            a[r.randrange(HH)] = 1
            return Weight(a, 'P')
        a = [1] * HH
        for _ in range(2):
            a[r.randrange(HH)] += r.randint(10, 500)
        return Weight(a, 'M')
    if sched == 'S':
        if not regime_next:
            return Weight([1] * HH, 'S-unif')
        Q = window_sums(xC, times[l], H, p ** (Dl + Dnext + 2))
        return q_star(Q, p, Dl, Dnext)
    raise ValueError(sched)


def regime(xC, mC, l):
    """R_{l+1} = {D_l + D_{l+1} <= m_l - M_{n_{l+2}}, M_{n_{l+2}} < m_l}, decided on the G_l-atom of xC.
    Returns (flag, D_l, D_{l+1}, M)."""
    n2 = times[l + 2]
    v, V, M = valdata(xC, p, n2)
    if M[n2] >= mC:
        return False, None, None, M[n2]
    Dl = V[times[l + 1]] - V[times[l]]
    Dn = V[n2] - V[times[l + 1]]
    return (Dl + Dn <= mC - M[n2]), Dl, Dn, M[n2]


def population_children(xp, pop_bits, pop_num, nl, nl1, mnew, R, q):
    """alive slope-0 children at n_{l+1} of the weighted slope-0 population at n_l, evaluated at xp."""
    mod = p ** R
    pi, dpi = pis(xp, p, nl1, mod)
    B = bits_to_matrix(pop_bits, nl)
    Se = (B @ pi[:nl]) % mod
    Sde = (B @ dpi[:nl]) % mod
    T = (FH @ pi[nl:nl1]) % mod
    Td = (FH @ dpi[nl:nl1]) % mod
    A1 = (Se[:, None] + T[None, :]) % mod
    al = (A1 % (p ** mnew)) == 0
    sl = ((Sde[:, None] + Td[None, :]) % p) != 0
    # W1(a) check: alive children of slope-0 parents are slope 0
    bad = int((al & ~sl).sum())
    ei, fi = np.nonzero(al)
    shift = np.uint64(nl)
    bits = pop_bits[ei] | (fi.astype(np.uint64) << shift)
    qa = np.array(q.a, dtype=object)
    num = pop_num[ei] * qa[fi]
    keep = np.array([t != 0 for t in num], dtype=bool) if len(num) else np.zeros(0, dtype=bool)
    return bits[keep], num[keep], bad, bits, num


def direct_population(xp, nl, mnew_check, R):
    """independent: all slope-0 alive paths at n_l at xp by BFS (used for measurability/survival checks)"""
    b, S, Sd = alive_all(xp, p, nl, R)
    return set(int(t) for t in b[(Sd % p) != 0])


def admissible(xA):
    v, V, M = valdata(xA, p, NMAX)
    m0 = V[times[0]]
    D0 = V[times[1]] - m0
    if not (M[times[1]] < m0 and D0 <= m0 - M[times[1]]):
        return None
    R = min(Rcap, m0 + 4 * L * (H // (p - 1) + 3) + 4)
    x0 = xA % p ** m0
    b, S, Sd = alive_all(x0, p, times[0], R)
    bits0 = b[(Sd % p) != 0]
    if len(bits0) == 0:
        return None
    return m0, R, x0, bits0


def run_atom(adm, sched, emode, keep_frac):
    m0, R, xA, bits0 = adm
    if psub is not None and len(bits0) > psub:
        idx = np.sort(np.array(random.Random(hseed(seed, 'psub', xA)).sample(range(len(bits0)), psub)))
        bits0 = bits0[idx]
    num0 = np.array([1] * len(bits0), dtype=object)
    root = dict(level=0, x=xA, m=m0, mu=Fraction(1), active=True, bits=bits0, num=num0, den=1, parent=None,
                Mt=Fraction(p ** m0 * len(bits0)), kids=[], keep=True, npos=len(bits0))
    levels = [[root]]
    w1a_bad = 0
    krnd = random.Random(hseed(seed, 'keep', xA, sched, emode))
    for l in range(0, L):
        nxt = []
        recs = []
        for nd in levels[l]:
            if not nd['active']:
                continue
            reg, Dl, Dn, Mn2 = regime(nd['x'], nd['m'], l)
            nd['reg_next'] = reg
            par = nd['parent']
            nd['q'] = choose_q(sched, l, nd['x'], nd['m'], par['x'] if par else None, par['m'] if par else None,
                               reg, Dl, Dn)
            vv, VV, MM = valdata(nd['x'], p, times[l + 1])
            assert MM[times[l + 1]] < nd['m'], "D_l undetermined on an active node"
            nd['D'] = VV[times[l + 1]] - VV[times[l]]
            if reg:
                assert Dl == nd['D']
                Q = window_sums(nd['x'], times[l], H, p ** (Dl + Dn + 2))
                nd['eps_t'] = eps_tilde(Q, nd['q'], p, Dl, Dn)
                nd['Dn'] = Dn
                recs.append(nd['eps_t'])
        vals = sorted(recs)
        if emode == 'inf' or not vals:
            ebar = None
        elif emode == 'med':
            ebar = vals[len(vals) // 2]
        elif emode == 'q1':
            ebar = vals[len(vals) // 4]
        elif emode == 'tiny':
            ebar = Fraction(0)
        else:
            raise ValueError(emode)
        STATS['ebar'][l + 1] = ebar
        for nd in levels[l]:
            if not nd['active']:
                c = dict(level=l + 1, x=nd['x'], m=nd['m'], mu=nd['mu'], active=False, bits=None, num=None,
                         den=nd['den'], parent=nd, Mt=nd['Mt'], kids=[], keep=False, frozen=True)
                nd['kids'].append(c)
                nxt.append(c)
                continue
            nd['B_next'] = nd['reg_next'] and (ebar is None or nd['eps_t'] <= ebar)
            nd['ebar_next'] = ebar
            Dl = nd['D']
            mnew = nd['m'] + Dl
            assert mnew + 1 <= R
            for t in range(p ** Dl):
                xp = nd['x'] + p ** nd['m'] * t
                bits, num, bad, _, _ = population_children(xp, nd['bits'], nd['num'], times[l], times[l + 1], mnew, R, nd['q'])
                w1a_bad += bad
                den = nd['den'] * nd['q'].den
                Mv = Fraction(p ** mnew * int(sum(num)) if len(num) else 0, den)
                act = nd['B_next']
                keep = act and (l + 1 < L or krnd.random() < keep_frac)
                c = dict(level=l + 1, x=xp % p ** mnew, m=mnew, mu=nd['mu'] / p ** Dl, active=act,
                         bits=bits if keep else None, num=num if keep else None, den=den, parent=nd, Mt=Mv,
                         kids=[], keep=keep, npos=len(bits))
                nd['kids'].append(c)
                nxt.append(c)
            if l >= 1 and not nd.get('meas_keep'):
                nd['bits'] = None
                nd['num'] = None
        cand = [c for c in nxt if c['active'] and c['bits'] is not None]
        for c in krnd.sample(cand, min(2, len(cand))):
            c['meas_keep'] = True
        levels.append(nxt)
    return levels, w1a_bad, R


def analyse(levels, sched, emode, tagA):
    # tau > l  <=>  node at level l active (for l <= L) ... active flag at level l means B_1..B_l hold
    # (1) martingale
    for l in range(0, L):
        for nd in levels[l]:
            if not nd['active']:
                continue
            kids = nd['kids']
            assert len(kids) == p ** nd['D']
            mean = sum((c['Mt'] for c in kids), Fraction(0)) / len(kids)
            chk('W6 martingale E[M_{l+1} | G_l] = M_l (W1, weighted)', mean == nd['Mt'], (tagA, l))
    # (2) first window: E_A[M~_1^2] <= M_0^2 (1 + chi^2_{q_0}(A))
    root = levels[0][0]
    a = [None] * (L + 1)
    for l in range(L + 1):
        a[l] = sum((nd['mu'] * nd['Mt'] ** 2 for nd in levels[l]), Fraction(0))
        chk('measures sum to 1', sum((nd['mu'] for nd in levels[l]), Fraction(0)) == 1, (tagA, l))
    M0 = root['Mt']
    Q0 = window_sums(root['x'], times[0], H, p ** (root['D'] + 2))
    chi = chi2(Q0, root['q'], p, root['D'])
    chk('W6 first window a_1 <= M_0^2 (1+chi^2_{q_0})', a[1] <= M0 ** 2 * (1 + chi), (tagA, a[1], M0 ** 2 * (1 + chi)))
    # (3) per-atom two-window inequality, l >= 1, on G_{l-1}-atoms C with tau > l
    ratios = []
    for l in range(1, L):
        for C in levels[l - 1]:
            if not C['active'] or not C.get('B_next'):
                continue
            kids = C['kids']
            gk = [g for k in kids for g in k['kids']]
            EM2 = sum((g['mu'] * g['Mt'] ** 2 for g in gk), Fraction(0)) / C['mu']
            EM1 = sum((k['mu'] * k['Mt'] ** 2 for k in kids), Fraction(0)) / C['mu']
            lhs = EM2 - EM1
            rhs = C['eps_t'] * C['Mt'] ** 2
            chk('W6 per-atom: E_C[M_{l+1}^2 - M_l^2] <= eps~_l M_{l-1}(C)^2 (W4)', lhs <= rhs, (tagA, l, lhs, rhs))
            if C['ebar_next'] is not None:
                chk('W6 per-atom: ... <= ebar_l M_{l-1}(C)^2', lhs <= C['ebar_next'] * C['Mt'] ** 2, (tagA, l))
            if rhs > 0:
                ratios.append(float(lhs / rhs))
            if sched == 'S' and C['reg_next']:
                Qs = window_sums(C['x'], times[l - 1], H, p ** (C['D'] + C['Dn'] + 2))
                mW, _, _ = m_W5(Qs, p, C['D'], C['Dn'])
                chk('Remark 2: with q* schedule eps~_l = m(W_{l-1};D_l)', C['eps_t'] == mW, (tagA, l, C['eps_t'], mW))
                if mW == 0:
                    okc = all(g['Mt'] == k['Mt'] for k in kids for g in k['kids'])
                    chk('Remark 2 / W5(c): m=0 => M_{l+1} = M_l on every G_l-atom', okc, (tagA, l))
                    STATS['S_m0_atoms'] = STATS.get('S_m0_atoms', 0) + 1
            if sched == 'P' and C['npos'] == 1:
                chk('W6 per-atom equality: single weighted path at C and point-mass q_l', lhs == rhs, (tagA, l, lhs, rhs))
            # sharp form for predictable schedules: q_l constant on C
            if sched in ('U', 'RP'):
                assert all('q' in k for k in kids)
                qs = set(tuple(Fraction(t, k['q'].den) for t in k['q'].a) for k in kids)
                chk('predictable schedule: q_l constant on the G_{l-1}-atom', len(qs) == 1, (tagA, l))
                k0 = kids[0]
                Dn = C['Dn']
                KK = C['D'] + Dn
                Qa = window_sums(C['x'], times[l - 1], H, p ** (KK + 2)) % p ** KK
                Qb = window_sums(C['x'], times[l], H, p ** (KK + 2)) % p ** KK
                PN = 1
                for s in range(1, H + 1):
                    PN *= (C['x'] + times[l - 1] + s)
                comp = (Qa[:, None] + (PN % p ** KK) * Qb[None, :]) % p ** KK
                es = eps_sharp(comp, C['q'], k0['q'], p, C['D'], Dn)
                chk('W6 predictable: ... <= eps^{q_{l-1},q_l} M_{l-1}(C)^2 (sharp W4)', lhs <= es * C['Mt'] ** 2, (tagA, l, lhs, es * C['Mt'] ** 2))
                chk('sharp eps <= eps~', es <= C['eps_t'], (tagA, l))
                if sched == 'U':
                    STATS['U_sharp_checked'] = STATS.get('U_sharp_checked', 0) + 1
    # (4) recursion for a_l and the product bound
    ebars = STATS['ebar']
    Pi = 1 + chi
    for l in range(1, L):
        eb = ebars.get(l)
        if eb is not None:
            chk('W6 recursion a_{l+1} - a_l <= ebar_l a_{l-1}', a[l + 1] - a[l] <= eb * a[l - 1], (tagA, l))
            Pi = Pi * (1 + eb)
        else:
            Pi = None
            break
        chk('W6 a_{l+1} <= M_0^2 Pi_{A,l}', a[l + 1] <= M0 ** 2 * Pi, (tagA, l))
    chk('a_l nondecreasing', all(a[i] <= a[i + 1] for i in range(L)), (tagA,))
    # (5) finite-horizon Paley-Zygmund
    if Pi is not None:
        # tau > L  <=>  level-L node active and its B_{L+1}? no: tau > L <=> B_1..B_L, i.e. node at level L active
        delta = sum((nd['mu'] for nd in levels[L] if not nd['active']), Fraction(0))
        Y = [(nd['mu'], nd['Mt'] if nd['active'] else Fraction(0)) for nd in levels[L]]
        EY = sum((mu * y for mu, y in Y), Fraction(0))
        EY2 = sum((mu * y * y for mu, y in Y), Fraction(0))
        muY = sum((mu for mu, y in Y if y > 0), Fraction(0))
        chk('PZ: E[Y_L^2] <= M_0^2 Pi', EY2 <= M0 ** 2 * Pi, (tagA,))
        lhsY = mpmath.mpf(EY.numerator) / EY.denominator
        bnd = mpmath.mpf(M0.numerator) / M0.denominator * (1 - mpmath.sqrt(mpmath.mpf(Pi.numerator) / Pi.denominator * mpmath.mpf(delta.numerator) / delta.denominator))
        chk('PZ: E[Y_L] >= M_0 (1 - sqrt(Pi delta))', lhsY >= bnd - mpmath.mpf(10) ** -30 * abs(bnd), (tagA, float(lhsY), float(bnd)))
        if Pi * delta < 1:
            pz = (1 - mpmath.sqrt(mpmath.mpf(Pi.numerator) / Pi.denominator * mpmath.mpf(delta.numerator) / delta.denominator)) ** 2 / (mpmath.mpf(Pi.numerator) / Pi.denominator)
            chk('W6 conclusion (finite horizon): mu_A(Y_L>0) >= (1-sqrt(Pi delta))^2/Pi',
                mpmath.mpf(muY.numerator) / muY.denominator >= pz - mpmath.mpf(10) ** -30, (tagA, float(muY), float(pz)))
            STATS.setdefault('pz_rows', []).append((tagA, float(muY), float(pz), float(delta), float(Pi)))
        else:
            STATS['pz_vacuous'] = STATS.get('pz_vacuous', 0) + 1
    return ratios, a


t0 = time.time()
done = 0
att = 0
allratios = []
meas_checks = 0
keep_frac = 0.02
while done < natoms and att < 3000 * natoms:
    att += 1
    kind = kinds[att % len(kinds)]
    if kind == 'rand':
        xA = rnd.randrange(p ** 40)
    elif kind == 'gate_hist':
        i = rnd.randint(1, n0)
        s = rnd.randint(2, 4)
        u = rnd.randrange(1, p ** 5)
        if u % p == 0:
            continue
        xA = (u * p ** s - i) % p ** 40
    else:
        raise ValueError(kind)
    adm = admissible(xA)
    if adm is None:
        continue
    done += 1
    m0, R, x0, bits_all = adm
    for sched in schedules:
        for emode in ebar_modes:
            STATS['ebar'] = {}
            levels, w1a_bad, R = run_atom(adm, sched, emode, keep_frac)
            tagA = (kind, x0, m0, sched, emode)
            chk('W1(a) along the chain: alive children of slope-0 parents have slope 0', w1a_bad == 0, (tagA, w1a_bad))
            ratios, a = analyse(levels, sched, emode, tagA)
            allratios += ratios
            nn = [len(lv) for lv in levels]
            nact = [sum(1 for nd in lv if nd['active']) for lv in levels]
            print(f"  atom {kind} x0={x0} m0={m0} sched={sched} ebar={emode} nodes/level={nn} active={nact} "
                  f"|P0 lines|={len(levels[0][0]['bits'])} a_l/M0^2={[round(float(t / levels[0][0]['Mt'] ** 2), 4) for t in a]}", flush=True)
            # measurability / survival on sampled nodes, at a second representative of the atom
            for l in range(1, L + 1):
                cand = [nd for nd in levels[l] if nd.get('meas_keep') and nd['bits'] is not None]
                for nd in cand:
                    alt = nd['x'] + p ** nd['m'] * rnd.randrange(1, p ** 3)
                    mine = set(int(t) for t in nd['bits'])
                    full_ok = psub is None and sched in ('U', 'R', 'RP', 'M')
                    if full_ok and len(bits_all) * (2 ** (H * l)) / p ** (nd['m'] - m0) < 3e5:
                        direct = direct_population(alt, times[l], nd['m'], R)
                        chk('MEAS: weighted population = full P^0_{n_l} at a 2nd representative (BFS)', mine == direct, (tagA, l))
                        if nd['Mt'] > 0:
                            chk('survival: M_l > 0 => some path alive at n_l (BFS)', len(direct) > 0, (tagA, l))
                    else:
                        # each weighted path is alive with slope 0 at the 2nd representative (exact big ints)
                        okall = True
                        for e in list(mine)[:400]:
                            s_ = 0
                            ds_ = 0
                            pi_ = 1
                            dpi_ = 0
                            for j in range(times[l]):
                                if (e >> j) & 1:
                                    s_ += pi_
                                    ds_ += dpi_
                                dpi_ = dpi_ * (alt + j + 1) + pi_
                                pi_ = pi_ * (alt + j + 1)
                            if s_ % p ** nd['m'] != 0 or ds_ % p == 0:
                                okall = False
                        chk('MEAS: weighted paths alive with slope 0 at a 2nd representative (exact)', okall, (tagA, l))
                    meas_checks += 1
                    if l < L and nd.get('reg_next') and 'q' in nd:
                        reg1, Dl1, Dn1, _ = regime(alt, nd['m'], l)
                        qalt = choose_q(sched, l, alt, nd['m'], nd['parent']['x'] if nd['parent'] else None,
                                        nd['parent']['m'] if nd['parent'] else None, reg1, Dl1, Dn1)
                        Qalt = window_sums(alt, times[l], H, p ** (Dl1 + Dn1 + 2))
                        chk('MEAS: eps~_{l+1} constant on the G_l-atom (stopping time is predictable)',
                            eps_tilde(Qalt, qalt, p, Dl1, Dn1) == nd['eps_t'], (tagA, l))
                    if sched == 'S' and l < L:
                        reg, Dl, Dn, _ = regime(alt, nd['m'], l)
                        reg0, Dl0, Dn0, _ = regime(nd['x'], nd['m'], l)
                        chk('MEAS: regime R_{l+1} constant on the G_l-atom', (reg, Dl, Dn) == (reg0, Dl0, Dn0), (tagA, l))
                        if reg and 'q' in nd:
                            q2 = choose_q('S', l, alt, nd['m'], None, None, reg, Dl, Dn)
                            chk('MEAS: q* constant on the G_l-atom',
                                [Fraction(t, q2.den) for t in q2.a] == [Fraction(t, nd['q'].den) for t in nd['q'].a], (tagA, l))
print(f"atoms: {done} attempts: {att} measurability samples: {meas_checks}")
print("checks:")
nf = 0
for name in sorted(CHK):
    print(f"  {name}: checks {CHK[name][0]} failures {CHK[name][1]}")
    nf += CHK[name][1]
if allratios:
    print(f"per-atom W4 ratio LHS/(eps~ M^2): max {max(allratios):.6g}, median {sorted(allratios)[len(allratios) // 2]:.4g}, n={len(allratios)}")
for r in STATS.get('pz_rows', [])[:20]:
    print("  PZ row (tag, mu_A(Y_L>0), bound, delta, Pi):", r)
print("S-schedule atoms with m=0 (complete coset):", STATS.get('S_m0_atoms', 0))
print("PZ vacuous (Pi*delta >= 1):", STATS.get('pz_vacuous', 0), " sharp-form checks with U:", STATS.get('U_sharp_checked', 0))
for f in FAILS[:10]:
    print("FAIL", f)
print(f"RESULT {'OK' if nf == 0 else 'FAIL'} failures={nf} time={time.time() - t0:.1f}s")
