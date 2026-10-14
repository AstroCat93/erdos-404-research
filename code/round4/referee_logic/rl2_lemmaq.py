"""Test (3): Lemma Q (M4A section 4; M4C section 3), from the statements only.

Usage:
  python3 rl2_lemmaq.py consts PMAX            (Q-a: constants, statistics)
  python3 rl2_lemmaq.py dp p SEED NU TMAX KMAX FMAX   (Q-b: inequality vs exact DP)
  python3 rl2_lemmaq.py summ p SEED NU TMAX     (Q-c: note's summary form, targeted)
  python3 rl2_lemmaq.py hist2 p SEED NU          (Q-d: chain rule at the 2nd 2D block)

Q-a  q_s(p) = p^s max_z P(sum_{r<p} d_r pi_r(-p) == z mod p^s) (M4A's form) by an
     exact residue DP, for primes p <= PMAX, s = 1, 2, 3 (s = 3 only p <= 23);
     M4C's q_2 via Phi = (A mod p, floor(A/p) - B mod p) by full enumeration of
     the 3^p digit vectors for p <= 13, and the identity
     sum d_r pi_r(-p) == A - pB (mod p^2) vector by vector.
Q-b  P(v(T)>=k, v(T')>=f), T = sum_{c<t} d_c pi_c(u), d_0 = 1, others lazy
     signed, by an exact integer DP over (T mod p^k, T' mod p^f), against
     M4A's bound (P_0 times block factors, 2D iff s_{r+1}=1 and
     L_{r+1} <= min(f, k - M_{r+1})) and, where f <= k - d_max, M4C's bound
     (exact per-block maxima, 2D blocks J).  Control: 2D factor q_2/p^3.
Q-c  The unconditional summary in note.md 12.1 ("every complete block ending
     at a depth-1 gate below the slope level contributes q_2/p^2"), i.e. the
     2D factor whenever s_{r+1}=1 and L_{r+1} <= f, WITHOUT L_{r+1} <= k-M_{r+1};
     a targeted search over points with a deep early gate and k close to f.
Q-d  Chain rule / independence: for points u whose blocks 1 and 2 both end
     at depth-1 gates, and for EVERY history h (digits of blocks 0 and 1) in
     A_0 & A_1, the set of block-2 digit vectors in A_2 = E^T_2 & E^R_3 (M4A)
     and in C^T_2 & C^T'_2 (M4C) is computed p-adically from the definitions
     of R_r and Y_i; checks P(.|h) <= q_2/p^2, that the set lies in one fibre
     of Z mod p^2 (resp. equals one fibre of Phi), and that the two events agree.
"""
import sys
KFMAX = 7
import random
import itertools
from fractions import Fraction
import numpy as np
from rl2_lib import v_p, harmonic_mod


def pi_int(y, c):
    r = 1
    for i in range(1, c + 1):
        r *= (y + i)
    return r


def q_dp(p, s):
    """q_s(p) exactly, by a DP over residues mod p^s (python ints)."""
    mod = p ** s
    law = {0: 1}
    for r in range(p):
        a = pi_int(-p, r) % mod
        new = {}
        for z, w in law.items():
            for d, wt in ((0, 2), (1, 1), (-1, 1)):
                key = (z + d * a) % mod
                new[key] = new.get(key, 0) + w * wt
        law = new
    return Fraction(mod * max(law.values()), 4 ** p)


def consts(pmax):
    primes = [q for q in range(5, pmax + 1) if all(q % d for d in range(2, q))]
    ok = True
    for p in primes:
        q1, q2 = q_dp(p, 1), q_dp(p, 2)
        line = f"p={p}: q1-1={float(q1 - 1):.4g} q2-1={float(q2 - 1):.4g}"
        if p <= 23:
            q3 = q_dp(p, 3)
            line += f" q3-1={float(q3 - 1):.4g}"
        if p in (7, 11):
            line += f"  [q1={q1}, q2={q2}]"
        if p <= 13:
            vecs = np.array(list(itertools.product((0, 1, -1), repeat=p)), dtype=np.int64)
            w = np.prod(np.where(vecs == 0, 2, 1), axis=1)
            fact = [1]
            for r in range(1, p):
                fact.append(fact[-1] * r)
            A = vecs @ np.array(fact, dtype=object)
            Bc = [fact[r] * harmonic_mod(r, p) % p for r in range(p)]
            B = vecs @ np.array(Bc, dtype=object)
            Z = vecs @ np.array([pi_int(-p, r) for r in range(p)], dtype=object)
            cnt = {}
            ident = True
            for a, b, z, ww in zip(A, B, Z, w):
                a, b, z = int(a), int(b), int(z)
                phi = (a % p, (a // p - b) % p)
                cnt[phi] = cnt.get(phi, 0) + int(ww)
                ident &= (z - (a - p * b)) % (p * p) == 0
            q2phi = Fraction(p * p * max(cnt.values()), 4 ** p)
            line += f"  Phi-form q2 equal: {q2phi == q2}; Z == A - pB mod p^2 for all 3^p vectors: {ident}"
            ok &= q2phi == q2 and ident
        print(line)
    print("RESULT:", "PASS" if ok else "FAILURE")


# ------------------------------------------------------------------ DP
def joint_prob(u, t, k, f, p):
    mk, mf = p ** k, p ** max(f, 0)
    # int64 is exact while 4^(t-1) < 2^62; otherwise python ints
    cur = np.zeros((mk, mf), dtype=np.int64 if t <= 31 else object)
    cur[1 % mk, 0] = 1
    cp, cd = 1, 0
    for c in range(1, t):
        cd = cd * (u + c) + cp
        cp = cp * (u + c)
        a, d = cp % mk, cd % mf
        cur = 2 * cur + np.roll(cur, (a, d), axis=(0, 1)) + np.roll(cur, (-a, -d), axis=(0, 1))
    return Fraction(int(cur[0, 0]), 4 ** (t - 1))


def P0(g, s, p):
    if s <= 0:
        return Fraction(1)
    if g == 1:
        return Fraction(0)
    tot = good = 0
    for v in itertools.product((0, 1, -1), repeat=g - 1):
        w = 1
        S = 1
        for c, d in enumerate(v, start=1):
            w *= 2 if d == 0 else 1
            S += d * pi_int(-g, c)
        tot += w
        good += w if S % p ** s == 0 else 0
    return Fraction(good, tot)


class Consts:
    def __init__(self, p, smax):
        self.p = p
        self.q = {s: q_dp(p, s) for s in range(1, smax + 1)}
        self.smax = smax
        self.p0 = {}

    def qd(self, d):
        if d <= self.smax:
            return self.q[d]
        return self.q[self.smax] * self.p ** (d - self.smax)     # q_s <= p q_{s-1}

    def P0(self, g, s):
        if (g, s) not in self.p0:
            self.p0[(g, s)] = P0(g, s, self.p)
        return self.p0[(g, s)]


def gate_data(u, t, p):
    gates = [g for g in range(1, t + 1) if (u + g) % p == 0]
    s = [v_p(u + g, p) for g in gates]
    L = [0]
    for x in s:
        L.append(L[-1] + x)
    Mr = [0]
    for x in s:
        Mr.append(max(Mr[-1], x))
    return gates, s, L, Mr


def m4a_bound(u, t, k, f, p, C, mode="m4a", twoD_factor=None):
    """M4A Lemma Q bound. mode='summary': drop L_{r+1} <= k - M_{r+1}."""
    gates, s, L, Mr = gate_data(u, t, p)
    if not gates:
        return None, 0
    b = C.P0(gates[0], min(s[0], k))
    n2 = 0
    tf = twoD_factor if twoD_factor is not None else C.q[2] / p ** 2
    for r in range(1, len(gates)):
        if L[r] >= k:
            break
        sn = s[r]
        cond = sn == 1 and L[r + 1] <= f
        if mode == "m4a":
            cond = cond and L[r + 1] <= k - Mr[r + 1]
        if cond:
            b *= tf
            n2 += 1
        else:
            d = min(sn, k - L[r])
            b *= C.qd(d) / p ** d
    return b, n2


def m4c_bound(u, t, k, f, p, C):
    """M4C Lemma Q bound (gates in [1,t-1]; exact per-block maxima)."""
    gates = [g for g in range(1, t) if (u + g) % p == 0]
    d = [v_p(u + g, p) for g in gates]
    I = len(gates)
    if I == 0:
        return None
    if not (1 <= f < k and f <= k - max(d)):
        return None
    ell = [0]
    for x in d:
        ell.append(ell[-1] + x)
    bnds = [0] + gates + [t]
    J = {i for i in range(1, I) if d[i] == 1 and ell[i] < f}
    res = Fraction(1)
    for i in range(I + 1):
        if ell[i] >= k:
            continue
        if i in J:
            res *= C.q[2] / p ** 2
            continue
        nxt = ell[i + 1] if i + 1 <= I else 10 ** 9
        e = min(nxt, k) - ell[i]
        mod = p ** e
        law = {0: 1}
        for c in range(bnds[i], bnds[i + 1]):
            a = (pi_int(u, c) // p ** ell[i]) % mod
            if c == 0:
                law = {(z + a) % mod: w for z, w in law.items()}
                continue
            new = {}
            for z, w in law.items():
                for dd, wt in ((0, 2), (1, 1), (-1, 1)):
                    key = (z + dd * a) % mod
                    new[key] = new.get(key, 0) + w * wt
            law = new
        res *= Fraction(max(law.values()), sum(law.values()))
    return res


def dp_test(p, seed, nu, tmax, kmax, fmax):
    rng = random.Random(seed)
    C = Consts(p, 5)
    n = viol_a = viol_c = n2d = ctl = nC = 0
    worst_a = worst_c = 0.0
    for it in range(nu):
        g1 = rng.randrange(2, p + 1)
        s1 = rng.choice([1, 1, 2, 3])
        y = rng.randrange(1, p ** 4)
        while y % p == 0:
            y = rng.randrange(1, p ** 4)
        u = p ** s1 * y - g1 + p ** 7 * rng.randrange(1, 30)
        if it % 3 == 2:                   # plant a depth-2/3 gate at g1 + p or g1 + 2p
            j = rng.choice([1, 2]); sd = rng.choice([2, 3])
            # adjust u modulo p^sd so that u + g1 + j p == 0 mod p^sd, keep u+g1 depth
            for _ in range(200):
                cand = u + p ** s1 * rng.randrange(0, p ** 4)
                if v_p(cand + g1, p) == s1 and v_p(cand + g1 + j * p, p) >= sd:
                    u = cand
                    break
        t = rng.randrange(g1 + p, tmax + 1)
        gates, s, L, Mr = gate_data(u, t, p)
        Vt = L[-1]
        if Vt < 1 or (u + g1) % p:
            continue
        if it % 2 == 0:                   # bias towards 2D blocks
            f = rng.randrange(2, fmax + 1)
            k = min(Vt, kmax, f + max(s) + rng.randrange(0, 2))
        else:
            k = rng.randrange(1, min(kmax, Vt) + 1)
            f = rng.randrange(1, fmax + 1)
        if k + max(f, 0) > (KFMAX if p <= 7 else KFMAX - 1) or k < 1:
            continue
        P = joint_prob(u, t, k, f, p)
        bA, two = m4a_bound(u, t, k, f, p, C)
        n += 1
        n2d += two > 0
        if P > bA:
            viol_a += 1
            print(f"  M4A VIOLATION u={u} t={t} k={k} f={f}: {P} > {bA}")
        if bA:
            worst_a = max(worst_a, float(P / bA))
        if two:
            bH, _ = m4a_bound(u, t, k, f, p, C, twoD_factor=C.q[2] / p ** 3)
            ctl += P > bH
        bC = m4c_bound(u, t, k, f, p, C)
        if bC is not None:
            nC += 1
            if P > bC:
                viol_c += 1
                print(f"  M4C VIOLATION u={u} t={t} k={k} f={f}: {P} > {bC}")
            if bC:
                worst_c = max(worst_c, float(P / bC))
    print(f"Q-b p={p} seed={seed}: {n} cases, {n2d} with a 2D block; M4C bound applicable in {nC}")
    print(f"  M4A bound violated {viol_a}; max P/bound {worst_a:.4f}")
    print(f"  M4C bound violated {viol_c}; max P/bound {worst_c:.4f}")
    print(f"  control (2D factor q2/p^3) violated in {ctl} of {n2d} cases with a 2D block")
    print("RESULT:", "PASS" if viol_a == 0 and viol_c == 0 else "FAILURE")


def summ_test(p, seed, nu, tmax):
    """Targeted: a deep gate early (block-0 end or first block end), then
    depth-1 gates; k small relative to the deep depth, f in (L_r, k)."""
    rng = random.Random(seed)
    C = Consts(p, 6)
    n = differ = viol = 0
    worst = 0.0
    for it in range(nu):
        g1 = rng.randrange(2, p + 1)
        sdeep = rng.randrange(2, 5)
        where = rng.choice([0, 1, 2])     # which gate is deep: g1, g1+p, g1+2p
        # u + g1 = p*y with v(y + where) = sdeep - 1 and y + i a unit for the
        # other i < 5, so the gates g1 + i p have depths 1 except one of depth sdeep
        z = rng.randrange(1, p ** 4)
        while z % p == 0:
            z = rng.randrange(1, p ** 4)
        y = -where + p ** (sdeep - 1) * z
        u = p * y - g1
        if u <= 0:
            continue
        gs = [v_p(u + g1 + i * p, p) for i in range(5)]
        if not (gs[where] == sdeep and all(gs[i] == 1 for i in range(5) if i != where)):
            continue                      # (only possible for p <= 3)
        t = rng.randrange(g1 + 2 * p, min(tmax, g1 + 4 * p) + 1)
        gates, s, L, Mr = gate_data(u, t, p)
        Vt = L[-1]
        cases = []
        for k in range(2, min(Vt, sdeep + 4) + 1):
            for f in range(1, k + 1):
                cases.append((k, f))
        for k, f in cases:
            bS, twoS = m4a_bound(u, t, k, f, p, C, mode="summary")
            bA, twoA = m4a_bound(u, t, k, f, p, C)
            if twoS == twoA or p ** (k + f) > 1_200_000:
                continue
            differ += 1
            P = joint_prob(u, t, k, f, p)
            n += 1
            if P > bS:
                viol += 1
                print(f"  SUMMARY-FORM VIOLATION u={u} t={t} gates={gates} depths={s} k={k} f={f}: "
                      f"P={P} ({float(P):.4g}) > summary bound {float(bS):.4g}; M4A bound {float(bA):.4g}")
            if bS:
                worst = max(worst, float(P / bS))
    print(f"Q-c p={p} seed={seed}: {differ} (u,k,f) cases where the summary form gives more 2D blocks than M4A's Lemma Q")
    print(f"  summary-form bound violated in {viol}; max P/summary-bound {worst:.4f}")
    print("RESULT:", "summary form NOT refuted" if viol == 0 else "summary form REFUTED")


# ------------------------------------------------------------------ Q-d
def to_res(fr, p, S, prec):
    """fr * p^S as an integer mod p^prec (fr*p^S must be p-integral)."""
    num, den = fr.numerator * p ** S, fr.denominator
    while den % p == 0:
        assert num % p == 0, "not p-integral after scaling"
        num //= p; den //= p
    return num * pow(den, -1, p ** prec) % p ** prec


def hist2(p, seed, nu):
    """Second 2D block: gates g1 (depth s1), g2=g1+p, g3=g1+2p, g4=g1+3p with
    depths s1, 1, 1, 1; k = L_4 + 1 (so blocks 1, 2 are 2D for M4A when
    f >= L_3 and k - M >= L_3), f = L_3."""
    rng = random.Random(seed)
    C = Consts(p, 2)
    bound = C.q[2] / p ** 2
    blocks = np.array(list(itertools.product((0, 1, -1), repeat=p)), dtype=np.int64)
    wblk = np.prod(np.where(blocks == 0, 2, 1), axis=1).astype(np.int64)
    Zb = blocks @ np.array([pi_int(-p, r) for r in range(p)], dtype=np.int64) % (p * p)
    fact = [1]
    for r in range(1, p):
        fact.append(fact[-1] * r)
    Ab = blocks @ np.array(fact, dtype=object)
    Bb = blocks @ np.array([fact[r] * harmonic_mod(r, p) % p for r in range(p)], dtype=object)
    Phib = np.array([(int(a) % p) * p + ((int(a) // p - int(b)) % p) for a, b in zip(Ab, Bb)])
    nh = 0
    okA = okC = agree = True
    worstA = worstC = Fraction(0)
    npts = 0
    for it in range(nu):
        g1 = rng.choice([2, 2, 3, 4])
        s1 = rng.choice([1, 1, 2])
        for _ in range(1000):
            u = p ** s1 * rng.randrange(1, p ** 6) - g1
            ds = [v_p(u + g1 + i * p, p) for i in range(4)]
            if ds == [s1, 1, 1, 1]:
                break
        else:
            continue
        g = [g1 + i * p for i in range(4)]          # g_1..g_4
        Lv = [0, s1, s1 + 1, s1 + 2, s1 + 3]          # L_0..L_4
        k = Lv[4] + 1
        f = Lv[3]
        # M4A 2D conditions for r = 1, 2: L_{r+1} <= min(f, k - M_{r+1})
        Mx = max(s1, 1)
        assert Lv[2] <= min(f, k - Mx) and Lv[3] <= min(f, k - Mx)
        # M4C hypothesis f <= k - d_max: d_max = max(s1, 1) (+ later gates < t)
        assert f <= k - Mx
        npts += 1
        cmax = g[2] + p                               # c < g_3 + ... we need c < g_3 for blocks <= 2
        top = g[2]                                    # blocks 0,1,2 are c < g_3
        Hc = [Fraction(0)]
        for c in range(1, top + 1):
            Hc.append(Hc[-1] + Fraction(1, u + c))
        pis = [Fraction(pi_int(u, c)) for c in range(top)]
        S = 6
        prec = k + 4 + S
        tco = [to_res(x, p, S, prec) for x in pis]
        # M4A: R^{<g_r}_r = sum_{c<g_r} d_c pi_c (pH_c - pH_{g_r})
        def Rco(r):
            gr = g[r - 1]
            return [to_res(pis[c] * p * (Hc[c] - Hc[gr]), p, S, prec) for c in range(gr)]
        R2, R3 = Rco(2), Rco(3)
        # M4C: Y_i = T'_0 + sum_{c in B_1..B_i} d pi h_c - sum_{i'=1}^{i+1} T_{<i'}/(u+g_{i'})
        hc = []
        for c in range(top):
            hc.append(sum((Fraction(1, u + j) for j in range(1, c + 1) if (u + j) % p), Fraction(0)))
        def Yco(i):
            co = []
            for c in range(g[i]):                      # c < g_{i+1}
                y = pis[c] * hc[c]
                for ip in range(1, i + 2):
                    if c < g[ip - 1]:
                        y -= pis[c] / (u + g[ip - 1])
                co.append(to_res(y, p, S, prec))
            return co
        Y1, Y2 = Yco(1), Yco(2)
        # histories: digits 1..g_2-1 (blocks 0 and 1), d_0 = 1
        nhist_digits = g[1] - 1
        H = np.array(list(itertools.product((0, 1, -1), repeat=nhist_digits)), dtype=np.int64)
        def lin(co, lo, hi, V):
            return (V @ np.array(co[lo:hi], dtype=object)) if hi > lo else np.zeros(len(V), dtype=object)
        hT1 = [tco[0] + int(x) for x in lin(tco, 1, g[0], H[:, :g[0] - 1])]        # T_{<g_1}
        hT2 = [tco[0] + int(x) for x in lin(tco, 1, g[1], H)]                        # T_{<g_2}
        hR2 = [R2[0] + int(x) for x in lin(R2, 1, g[1], H)]
        hY1 = [Y1[0] + int(x) for x in lin(Y1, 1, g[1], H)]
        hR3 = [R3[0] + int(x) for x in lin(R3, 1, g[1], H)]
        hY2 = [Y2[0] + int(x) for x in lin(Y2, 1, g[1], H)]
        bT = [int(x) for x in lin(tco, g[1], g[2], blocks)]
        bR3 = [int(x) for x in lin(R3, g[1], g[2], blocks)]
        bY2 = [int(x) for x in lin(Y2, g[1], g[2], blocks)]
        mod = p ** prec
        bT = np.array(bT, dtype=object) % mod
        bR3 = np.array(bR3, dtype=object) % mod
        bY2 = np.array(bY2, dtype=object) % mod
        sc = p ** S
        tot = int(wblk.sum())
        for hi in range(len(H)):
            # A_0 = {v(T_{<g1}) >= min(L_1,k)}; A_1 = E^T_1 & E^R_2 (block 1 is 2D)
            if (hT1[hi] % mod) % (sc * p ** Lv[1]) != 0:
                continue
            if (hT2[hi] % mod) % (sc * p ** Lv[2]) != 0:
                continue
            A1 = (hR2[hi] % mod) % (sc * p ** (Lv[2] + 1)) == 0
            C1 = (hY1[hi] % mod) % (sc * p ** (Lv[1] + 1)) == 0
            if A1 != C1:
                agree = False
            if not A1:
                continue
            nh += 1
            okT = ((hT2[hi] + bT) % mod) % (sc * p ** Lv[3]) == 0          # E^T_2 / C^T_2
            okR = ((hR3[hi] + bR3) % mod) % (sc * p ** (Lv[3] + 1)) == 0   # E^R_3
            okY = ((hY2[hi] + bY2) % mod) % (sc * p ** (Lv[2] + 1)) == 0   # C^T'_2
            selA = np.array([bool(a and b) for a, b in zip(okT, okR)])
            selC = np.array([bool(a and b) for a, b in zip(okT, okY)])
            pA = Fraction(int(wblk[selA].sum()), tot)
            pC = Fraction(int(wblk[selC].sum()), tot)
            worstA = max(worstA, pA); worstC = max(worstC, pC)
            if len(set(Zb[selA].tolist())) > 1:
                okA = False
            if selC.any():
                fib = set(Phib[selC].tolist())
                if len(fib) != 1 or not np.array_equal(np.isin(Phib, list(fib)), selC):
                    okC = False
            if not np.array_equal(selA, selC):
                agree = False
    print(f"Q-d p={p} seed={seed}: {npts} points, {nh} histories in A_0 & A_1 (block 1 already 2D)")
    print(f"  max_h P(A_2 | h) [M4A: E^T_2 & E^R_3]    = {float(worstA):.6g}  (q2/p^2 = {float(bound):.6g})")
    print(f"  max_h P(C^T_2 & C^T'_2 | h) [M4C]       = {float(worstC):.6g}")
    print(f"  M4A event in one fibre of Z mod p^2 for every h: {okA}; M4C event = one fibre of Phi: {okC}; "
          f"events agree (blocks 1 and 2): {agree}")
    ok = worstA <= bound and worstC <= bound and okA and okC
    print("RESULT:", "PASS" if ok else "FAILURE")


if __name__ == "__main__":
    mode = sys.argv[1]
    a = [int(x) for x in sys.argv[2:]]
    {"consts": consts, "dp": dp_test, "summ": summ_test, "hist2": hist2}[mode](*a)
