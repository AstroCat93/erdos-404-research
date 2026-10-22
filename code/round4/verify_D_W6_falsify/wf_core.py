"""Core library for the numerical-falsification check of M4D's Lemmas W1-W3, Prop W4, Cor W5, Thm W6.

Written from the definitions in data/round4/reports/M4D.md section 3 and data/round3/reports/R3M.md
sections 1-5.  Shares no code with code/round4/M4D/, code/round4/verify_M4D_logic/ or
code/round4/verify_M4D_falsify/.

Conventions
-----------
* x is a natural number (a genuine point of Z_p that is not a negative integer).
* pi_j(x) = (x+1)...(x+j), pi_0 = 1.  A path e of length n is a 0/1 word with e_0 = 1,
  S_e = sum_{j<n} e_j pi_j.  e is alive at n iff v_p(S_e(x)) >= V_n(x).  slope = v_p(S_e'(x)).
* "Brute" side: populations are found by a pruned breadth-first search on exact residues of S_e
  (complete, because a prefix of an alive path is alive) and then by direct evaluation of
  S_{(e,f)}(x'), S_{(e,f,f')}(x') and their derivatives at every point x' = x0 + p^m w of the
  cylinder, w running over Z/p^K.  Nothing on the brute side uses Lemma 2, Prop B or Lemma C1.
* "Formula" side: the quantities in the statements (mu^q, chi^2_q, eps-tilde^q, eps^{q,q'},
  F^q, m(W;D'), q*) computed from the window sums Q_f(x) exactly.
* All comparisons that are claimed as identities or inequalities between rationals are done in
  exact rational arithmetic (fractions.Fraction / Python ints).  Per-frequency statements
  (W3(b) per xi) are cosine sums with exact rational coefficients, evaluated with mpmath at 50
  significant digits.
"""
import numpy as np
from fractions import Fraction
import mpmath

mpmath.mp.dps = 50


def vp(a, p):
    if a == 0:
        raise ValueError("valuation of 0")
    v = 0
    while a % p == 0:
        a //= p
        v += 1
    return v


def valdata(x, p, Nmax):
    """v(x+i), V_i, M_i for i = 0..Nmax (index 0 unused / zero)."""
    v = [0] * (Nmax + 1)
    V = [0] * (Nmax + 1)
    M = [0] * (Nmax + 1)
    for i in range(1, Nmax + 1):
        v[i] = vp(x + i, p)
        V[i] = V[i - 1] + v[i]
        M[i] = max(M[i - 1], v[i])
    return v, V, M


def pis(x, p, Nmax, mod):
    """pi_j(x) mod `mod` and pi_j'(x) mod `mod` for j = 0..Nmax, as int64 arrays (exact Python-int recursion)."""
    pi = [1 % mod]
    dpi = [0]
    for j in range(1, Nmax + 1):
        dpi.append((dpi[-1] * (x + j) + pi[-1]) % mod)
        pi.append((pi[-1] * (x + j)) % mod)
    return np.array(pi, dtype=np.int64), np.array(dpi, dtype=np.int64)


def digits(H):
    """All words f in {0,1}^H as a (2^H, H) int64 matrix; row index = sum f_i 2^i."""
    idx = np.arange(1 << H, dtype=np.int64)
    return ((idx[:, None] >> np.arange(H, dtype=np.int64)[None, :]) & 1).astype(np.int64)


def bits_to_matrix(bits, n):
    sh = np.arange(n, dtype=np.uint64)
    return ((bits[:, None] >> sh[None, :]) & np.uint64(1)).astype(np.int64)


def alive_all(x, p, n, R):
    """All paths of length n alive at n for x (all slopes), by pruned BFS on exact residues mod p^R.
    Returns (bits uint64, S mod p^R, S' mod p^R)."""
    mod = p ** R
    assert mod < 2 ** 56
    v, V, M = valdata(x, p, n)
    assert R >= V[n]
    pi, dpi = pis(x, p, n, mod)
    if V[1] > 0:
        z = np.zeros(0, dtype=np.int64)
        return np.zeros(0, dtype=np.uint64), z, z
    bits = np.ones(1, dtype=np.uint64)
    S = np.ones(1, dtype=np.int64)
    Sd = np.zeros(1, dtype=np.int64)
    for j in range(1, n):
        b1 = bits | (np.uint64(1) << np.uint64(j))
        S1 = (S + pi[j]) % mod
        Sd1 = (Sd + dpi[j]) % mod
        bits = np.concatenate([bits, b1])
        S = np.concatenate([S, S1])
        Sd = np.concatenate([Sd, Sd1])
        keep = (S % (p ** V[j + 1])) == 0
        bits, S, Sd = bits[keep], S[keep], Sd[keep]
    return bits, S, Sd


def brute_alive_check(x, p, n):
    """Exhaustive check of alive_all for small n: all 2^(n-1) paths, exact big-integer S_e(x)."""
    v, V, M = valdata(x, p, n)
    pi = [1]
    for j in range(1, n):
        pi.append(pi[-1] * (x + j))
    out = set()
    for mask in range(1 << (n - 1)):
        e = 1 | (mask << 1)
        s = sum(pi[j] for j in range(n) if (e >> j) & 1)
        if s % (p ** V[n]) == 0:
            out.add(e)
    return out


def inv(a, p, k):
    return pow(int(a) % p ** k, -1, p ** k) if k > 0 else 0


# ----------------------------------------------------------------------------------------------
# formula side
# ----------------------------------------------------------------------------------------------

def hist(res, weights, size):
    """Exact histogram: sum of Python-int weights per residue."""
    out = [0] * size
    for r, w in zip(res.tolist(), weights):
        if w:
            out[r] += w
    return out


def coll_num(h):
    return sum(c * c for c in h)


class Weight:
    """A probability vector on {0,1}^H stored as integer numerators `a` (Python ints) and denominator."""

    def __init__(self, a, name=""):
        a = [int(t) for t in a]
        assert all(t >= 0 for t in a) and sum(a) > 0
        self.a = a
        self.den = sum(a)
        self.name = name

    @staticmethod
    def from_fractions(fr, name=""):
        from math import lcm
        L = 1
        for t in fr:
            L = lcm(L, Fraction(t).denominator)
        return Weight([int(Fraction(t) * L) for t in fr], name)

    def frac(self, i):
        return Fraction(self.a[i], self.den)


def mu_hist(Q, wt, p, k):
    """numerators of mu^q_k (denominator wt.den)"""
    return hist(Q % (p ** k), wt.a, p ** k)


def eps_tilde(Q, wt, p, D, D2):
    K = D + D2
    hK = mu_hist(Q, wt, p, K)
    hD = mu_hist(Q, wt, p, D)
    return Fraction(p ** K * coll_num(hK) - p ** D * coll_num(hD), wt.den ** 2)


def chi2(Q, wt, p, D):
    hD = mu_hist(Q, wt, p, D)
    return Fraction(p ** D * coll_num(hD), wt.den ** 2) - 1


def eps_sharp(comp, wt, wt2, p, D, D2):
    """comp[f, f'] = (Q_f + (pi_N/pi_n) Q'_{f'}) mod p^K : composite sums.  nu = law under q x q'."""
    K = D + D2
    PK = p ** K
    h = [0] * PK
    a = wt.a
    b = wt2.a
    for i in range(len(a)):
        if a[i] == 0:
            continue
        row = comp[i].tolist()
        ai = a[i]
        for j, r in enumerate(row):
            if b[j]:
                h[r] += ai * b[j]
    hD = [0] * (p ** D)
    for r, c in enumerate(h):
        if c:
            hD[r % (p ** D)] += c
    den = (wt.den * wt2.den) ** 2
    return Fraction(p ** K * coll_num(h) - p ** D * coll_num(hD), den)


def lift_data(Q, p, D, D2):
    """Sigma = {Q_f mod p^K}; |Lift(r)| for r in Z/p^D; representatives count per residue."""
    K = D + D2
    resK = Q % (p ** K)
    sig, cnt = np.unique(resK, return_counts=True)
    nrep = dict(zip(sig.tolist(), cnt.tolist()))
    lift = [0] * (p ** D)
    for s in sig.tolist():
        lift[s % (p ** D)] += 1
    return lift, nrep


def m_W5(Q, p, D, D2):
    lift, nrep = lift_data(Q, p, D, D2)
    P2 = p ** D2
    if any(L == P2 for L in lift):
        return Fraction(0), lift, nrep
    s = Fraction(0)
    for L in lift:
        if L > 0:
            s += Fraction(L, P2 - L)  # 1/a_r with a_r = P2/L - 1 = (P2-L)/L
    return Fraction(p ** D) / s, lift, nrep


def q_star(Q, p, D, D2):
    lift, nrep = lift_data(Q, p, D, D2)
    P2 = p ** D2
    PD = p ** D
    K = D + D2
    complete = [r for r in range(PD) if lift[r] == P2]
    nu = [Fraction(0)] * PD
    if complete:
        for r in complete:
            nu[r] = Fraction(1, len(complete))
    else:
        inva = [Fraction(L, P2 - L) if L > 0 else Fraction(0) for L in lift]
        S = sum(inva)
        nu = [t / S for t in inva]
    fr = []
    for qf in Q.tolist():
        s = qf % (p ** K)
        r = s % PD
        if nu[r] == 0:
            fr.append(Fraction(0))
        else:
            fr.append(nu[r] / lift[r] / nrep[s])
    assert sum(fr) == 1
    return Weight.from_fractions(fr, "qstar")


# ----------------------------------------------------------------------------------------------
# cylinder data (brute side)
# ----------------------------------------------------------------------------------------------

def segsum(vals, keys_sorted, nW):
    """exact per-key sums of vals (keys sorted ascending, 0 <= key < nW); returns list of Python ints"""
    cnt = np.bincount(keys_sorted, minlength=nW)
    out = [0] * nW
    if len(vals) == 0:
        return out
    starts = np.concatenate([[0], np.cumsum(cnt)[:-1]])
    nz = np.nonzero(cnt)[0]
    red = np.add.reduceat(vals, starts[nz])
    for k, s in zip(nz.tolist(), red.tolist()):
        out[k] = int(s)
    return out


class Cyl:
    """Cylinder C = x + p^m Z_p, m = V_n(x), windows W = [n,N), W' = [N,N').  Enumerates w mod p^Kenum.

    Stores, for every w, the alive slope-0 children of the slope-0 parents (brute force) and their
    alive slope-0 children in W', plus targets.  Also runs the W1(a) structural checks."""

    def __init__(self, p, x, n, H, H2, kextra=0, check_parents_at=3, rng=None, psub=None, full_children=False):
        self.p, self.x, self.n, self.H, self.H2 = p, x, n, H, H2
        N = n + H
        N2 = N + H2
        self.N, self.N2 = N, N2
        v, V, M = valdata(x, p, N2)
        self.v, self.V, self.M = v, V, M
        m = V[n]
        D = V[N] - m
        D2 = V[N2] - V[N]
        self.m, self.D, self.D2, self.K = m, D, D2, D + D2
        self.cond52 = (D + D2 <= m - M[N2]) and (M[N2] < m)
        self.cond51max = m - M[N] - D  # largest k allowed by (5.1)
        self.ok = self.cond52
        if not self.ok:
            return
        K = self.K
        # enumeration depth: K, or D + k for W3 tests with k = D2 + kextra if (5.1) permits
        k3 = min(D2 + kextra, self.cond51max) if kextra > 0 else D2
        self.k3 = k3
        Ken = max(K, D + k3)
        self.Ken = Ken
        R = m + Ken + 1
        self.R = R
        mod = p ** R
        self.mod = mod
        x0 = x % (p ** m)
        self.x0 = x0
        bits, S, Sd = alive_all(x0, p, n, R)
        self.nalive_all = len(bits)
        B = bits_to_matrix(bits, n)
        sl0 = (Sd % p) != 0
        self.sl0 = sl0
        if rng is None:
            rng = np.random.default_rng(12345)
        # lines followed to N': all slope-0 parents, or a random subset of size psub (the others get
        # weight 0, which the lemmas allow); plus up to psub parents of positive slope (W1(a) at N')
        i0 = np.nonzero(sl0)[0]
        ihi = np.nonzero(~sl0)[0]
        if psub is not None and len(i0) > psub:
            i0 = np.sort(rng.choice(i0, size=psub, replace=False))
        if psub is not None and len(ihi) > psub:
            ihi = np.sort(rng.choice(ihi, size=psub, replace=False))
        sel0 = np.zeros(len(bits), dtype=bool)
        sel0[i0] = True
        selhi = np.zeros(len(bits), dtype=bool)
        selhi[ihi] = True
        self.sel0 = sel0
        self.bits0 = bits[sel0]
        self.S0 = S[sel0]
        self.Sd0 = Sd[sel0]
        self.P = int(sel0.sum())
        self.P0_all = int(sl0.sum())
        if self.P == 0:
            return  # empty slope-0 population: nothing to test (the samplers reject such cylinders)
        if psub is not None and not full_children:
            # large populations: evaluate only the sampled lines (W1(a) checks then cover these lines)
            keepi = sel0 | selhi
            B = B[keepi]
            sl0 = sl0[keepi]
            sel0 = sel0[keepi]
            selhi = selhi[keepi]
        FH = digits(H)
        FH2 = digits(H2)
        self.FH, self.FH2 = FH, FH2
        pm = p ** m
        pmD = p ** (m + D)
        pmK = p ** (m + K)
        pD2 = p ** D2
        pk3 = p ** k3
        self.stats = dict(w1a_child_slope_bad=0, w1a_hi_child_slope0=0, w1a_gchild_bad=0,
                          parent_const_bad=0, parent_set_bad=0, children_total=0, gchildren_total=0,
                          parent_set_checked=0)
        chw, che, chf, chtau = [], [], [], []
        gcw, gcc, gcf = [], [], []
        nch = 0
        chk_w = set(rng.integers(0, p ** Ken, size=check_parents_at).tolist())
        pidx = np.cumsum(sel0) - 1
        # locality: a few points are evaluated twice, at w and at w + p^Ken * r (same class mod p^Ken);
        # the alive structures must coincide (populations depend on w mod p^Ken only)
        loc_w = set(rng.integers(0, p ** Ken, size=2).tolist())
        self.stats['locality_checked'] = 0
        self.stats['locality_bad'] = 0
        wlist = list(range(p ** Ken))
        extra = [(w, w + p ** Ken * int(rng.integers(1, p ** 4))) for w in sorted(loc_w)]
        ref = {}
        for w, wbig in [(w, w) for w in wlist] + extra:
            xp = x0 + pm * wbig
            pi, dpi = pis(xp, p, N2, mod)
            Se = (B @ pi[:n]) % mod
            Sde = (B @ dpi[:n]) % mod
            # Lemma 2(a): aliveness and slope of parents constant on C
            if not np.all(Se % pm == 0) or not np.array_equal((Sde % p) != 0, sl0):
                self.stats['parent_const_bad'] += 1
            if w in chk_w:
                b2, _, _ = alive_all(xp, p, n, R)
                self.stats['parent_set_checked'] += 1
                if not np.array_equal(np.sort(b2), np.sort(bits)):
                    self.stats['parent_set_bad'] += 1
            T = (FH @ pi[n:N]) % mod
            Td = (FH @ dpi[n:N]) % mod
            A1 = (Se[:, None] + T[None, :]) % mod
            al1 = (A1 % pmD) == 0
            s1 = ((Sde[:, None] + Td[None, :]) % p) != 0
            # W1(a): alive children of slope-0 parents have slope 0; of slope>0 parents have slope>0
            self.stats['w1a_child_slope_bad'] += int((al1 & ~s1)[sl0].sum())
            self.stats['w1a_hi_child_slope0'] += int((al1 & s1)[~sl0].sum())
            ei, fi = np.nonzero(al1 & (sel0 | selhi)[:, None])
            Sc = A1[ei, fi]
            Sdc = (Sde[ei] + Td[fi]) % mod
            csl0 = sl0[ei]
            T2 = (FH2 @ pi[N:N2]) % mod
            Td2 = (FH2 @ dpi[N:N2]) % mod
            A2 = (Sc[:, None] + T2[None, :]) % mod
            al2 = (A2 % pmK) == 0
            s2 = ((Sdc[:, None] + Td2[None, :]) % p) != 0
            # grandchildren have slope 0 iff the line (parent) has slope 0
            self.stats['w1a_gchild_bad'] += int((al2 & (s2 != csl0[:, None])).sum())
            keep = csl0
            ei0 = ei[keep]
            fi0 = fi[keep]
            Sc0 = Sc[keep]
            e_idx = pidx[ei0]
            piN = int(pi[N])
            assert piN % pmD == 0 and (piN // pmD) % p != 0
            if k3 > 0:
                uN = inv(piN // pmD, p, k3)
                tau = (((-(Sc0 // pmD)) % pk3) * uN) % pk3
            else:
                tau = np.zeros_like(Sc0)
            al2k = al2[keep]
            ci, f2i = np.nonzero(al2k)
            if w != wbig:
                self.stats['locality_checked'] += 1
                r0 = ref[w]
                if not (np.array_equal(r0[0], e_idx) and np.array_equal(r0[1], fi0) and np.array_equal(r0[2], tau)
                        and np.array_equal(r0[3], ci) and np.array_equal(r0[4], f2i)):
                    self.stats['locality_bad'] += 1
                continue
            if w in loc_w:
                ref[w] = (e_idx.copy(), fi0.copy(), tau.copy(), ci.copy(), f2i.copy())
            chw.append(np.full(len(ei0), w, dtype=np.int64)); che.append(e_idx); chf.append(fi0); chtau.append(tau)
            gcw.append(np.full(len(ci), w, dtype=np.int64)); gcc.append(ci + nch); gcf.append(f2i)
            nch += len(ei0)
        self.ch_w = np.concatenate(chw); self.ch_e = np.concatenate(che).astype(np.int64)
        self.ch_f = np.concatenate(chf).astype(np.int64); self.ch_tau = np.concatenate(chtau).astype(np.int64)
        self.gc_w = np.concatenate(gcw); self.gc_c = np.concatenate(gcc).astype(np.int64)
        self.gc_f = np.concatenate(gcf).astype(np.int64)
        self.stats['children_total'] = len(self.ch_w)
        self.stats['gchildren_total'] = len(self.gc_w)
        self.nW = p ** Ken
        # ---------------- formula side --------------------------------------------------
        y = [1]
        for i in range(1, H):
            y.append(y[-1] * (x + n + i))
        y2 = [1]
        for i in range(1, H2):
            y2.append(y2[-1] * (x + N + i))
        PN = 1
        for s in range(1, H + 1):
            PN *= (x + n + s)
        assert vp(PN, p) == D
        self.PN = PN
        BIG = p ** (Ken + 2)
        self.Q = np.array([sum(y[i] for i in range(H) if (fidx >> i) & 1) % BIG for fidx in range(1 << H)],
                          dtype=np.int64)
        self.Q2 = np.array([sum(y2[i] for i in range(H2) if (fidx >> i) & 1) % BIG for fidx in range(1 << H2)],
                           dtype=np.int64)
        PK = p ** K
        Qk = self.Q % PK
        Q2k = self.Q2 % PK
        self.comp = (Qk[:, None] + (PN % PK) * Q2k[None, :]) % PK
        self.u = (PN // p ** D)
        # Prop B / W2 data at x0 for slope-0 parents
        pi0 = 1
        for i in range(1, n + 1):
            pi0 *= (x0 + i)
        assert vp(pi0, p) == m
        omega = (pi0 // pm)
        PDm = p ** Ken
        oinv = inv(omega, p, Ken)
        S0 = [int(s) for s in self.S0]
        Sd0 = [int(s) for s in self.Sd0]
        # S_e(x0) mod p^R; S_e(x0)/p^m mod p^{R-m}
        self.tau0 = [(-(s // pm) * oinv) % PDm for s in S0]   # tau_n(e,x0) mod p^Ken
        self.beta = [(oinv * sd) % PDm for sd in Sd0]          # omega^{-1} S'_e(x0) mod p^Ken

    # ------------------------------------------------------------------------------------------
    def cprime(self, w):
        """index of the sub-cylinder C' (x' mod p^{m+D}) of enumeration point w"""
        return w % (self.p ** self.D)

    def sums(self, wpar, q, btab):
        """Exact integer sums: sN[w] = sum_{children (e,f) at w} wpar[e] a[f];
        sN2[w] = sum_{grandchildren (e,f,f')} wpar[e] a[f] b_{C'(w)}[f'].
        btab: list over C'-indices of Weight on W'.  Returns Python-int lists and the per-child products."""
        nW = self.nW
        big = max(list(wpar) + [1]) * max(q.a) * max(max(t.a) for t in btab) * max(1, len(self.gc_w), len(self.ch_w))
        dt = np.int64 if big < 2 ** 62 else object
        wp = np.array(wpar, dtype=dt)
        a = np.array(q.a, dtype=dt)
        prod = wp[self.ch_e] * a[self.ch_f] if len(self.ch_e) else np.zeros(0, dtype=dt)
        sN = segsum(prod, self.ch_w, nW)
        B = np.array([t.a for t in btab], dtype=dt)
        cp = self.gc_w % (self.p ** self.D)
        prod2 = prod[self.gc_c] * B[cp, self.gc_f] if len(self.gc_c) else np.zeros(0, dtype=dt)
        sN2 = segsum(prod2, self.gc_w, nW)
        return sN, sN2, prod

    def moments(self, wpar, q, btab):
        """Exact E_C[M_N], E_C[M_N^2], E_C[M_N'], E_C[M_N'^2], per-C' data, M_n."""
        p, m, D, K = self.p, self.m, self.D, self.K
        sN, sN2, prod = self.sums(wpar, q, btab)
        nW = self.nW
        nC = p ** D
        Aden = q.den
        cfac = [Fraction(p ** (m + K), Aden * btab[c].den) for c in range(nC)]
        MN = [Fraction(p ** (m + D) * s, Aden) for s in sN]
        MN2 = [cfac[w % nC] * sN2[w] for w in range(nW)]
        Mn = p ** m * sum(wpar)
        return MN, MN2, Mn
