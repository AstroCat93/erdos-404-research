"""Exact tests of Lemma Q (M4A section 4 and M4C section 3), written from the
statements only.

Usage:
  python3 rl_lemmaq.py consts  p               (Q1: q_s, P_0, block statistic)
  python3 rl_lemmaq.py hist    p SEED NU        (Q3: per-history 2D step)
  python3 rl_lemmaq.py dp      p SEED NU KMAX FMAX TMAX   (Q2: full DP)

Q1  Enumerates all 3^p lazy signed vectors (weights 2,1,1).  Computes
    q_s = p^s max_z P(Z == z mod p^s), Z = sum_k zeta_k pi_k(-p) (M4A), and
    q_2 via M4C's statistic Phi = (A mod p, floor(A/p) - B mod p),
    A = sum zeta_r r!, B = sum zeta_r r! H_r.  Checks that Z mod p^2 and Phi
    determine each other (a bijection on the support), hence equal q_2.
Q3  The heart of the chain rule.  For a point u whose first two gates are
    g_1 (depth s_1) and g_2 = g_1 + p (depth 1), and for EVERY history h of
    block 0 (digits delta_1..delta_{g_1-1}, delta_0 = 1) lying in A_0:
      M4A: the set of block-1 configurations in E^T_1 & E^R_2 is contained in
           one fibre of Z mod p^2, so P(.|h) <= q_2/p^2;
      M4C: the set in C^T_1 & C^T'_1 (Y_1 == 0 mod p^{l_1+1}) is exactly one
           fibre of Phi (or empty), so P(.|h) <= q_2/p^2.
    Everything is computed p-adically from the definitions (R_r, Y_i).
Q2  Exact DP of P(v(T) >= k, v(T') >= f), T = sum_{c<t} delta_c pi_c(u),
    delta_0 = 1, compared with the M4A bound and (when its hypothesis
    f <= k - d_max holds) the M4C bound.  Controls: (i) 2D factor q_2/p^3;
    (ii) the informal summary of note.md 12.1 (2D factor for every full block
    ending at a depth-1 gate at level <= f, ignoring L_{r+1} <= k - M_{r+1}).
"""
import sys
import random
import itertools
from fractions import Fraction
import numpy as np
from rl_lib import vp, V


def signed_configs(n):
    """All 3^n vectors in {0,1,-1}^n with weights (2,1,1) products."""
    vals = np.array(list(itertools.product((0, 1, -1), repeat=n)), dtype=np.int64)
    w = np.prod(np.where(vals == 0, 2, 1), axis=1)
    return vals, w


def pi_int(y, c):
    r = 1
    for i in range(1, c + 1):
        r *= (y + i)
    return r


def harmonic_mod(r, p):
    return sum(pow(s, -1, p) for s in range(1, r + 1)) % p


def consts(p, smax=3, verbose=True):
    vals, w = signed_configs(p)
    tot = int(w.sum())
    coef = [pi_int(-p, k) for k in range(p)]
    Z = vals @ np.array(coef, dtype=object)
    q = {}
    for s in range(1, smax + 1):
        mod = p ** s
        cnt = {}
        for z, ww in zip(Z, w):
            key = int(z) % mod
            cnt[key] = cnt.get(key, 0) + int(ww)
        q[s] = Fraction(mod * max(cnt.values()), tot)
    fact = [1]
    for r in range(1, p):
        fact.append(fact[-1] * r)
    A = vals @ np.array(fact, dtype=object)
    Bc = [(fact[r] * harmonic_mod(r, p)) % p for r in range(p)]
    B = (vals @ np.array(Bc, dtype=object))
    phi_of_z = {}
    z_of_phi = {}
    bij = True
    cntphi = {}
    for a, b, z, ww in zip(A, B, Z, w):
        a = int(a); b = int(b); z = int(z) % (p * p)
        phi = (a % p, ((a // p) - b) % p)
        if phi_of_z.setdefault(z, phi) != phi or z_of_phi.setdefault(phi, z) != z:
            bij = False
        cntphi[phi] = cntphi.get(phi, 0) + int(ww)
    q2phi = Fraction(p * p * max(cntphi.values()), tot)
    if verbose:
        for s in q:
            print(f"  q_{s}({p}) = {q[s]} = {float(q[s]):.12g}")
        print(f"  q_2 via Phi = {q2phi}; equal to q_2 via Z: {q2phi == q[2]}; "
              f"Z mod p^2 <-> Phi bijective on support: {bij}")
        print(f"  monotone q_1 <= q_2 <= q_3 and q_s <= p q_(s-1): "
              f"{q[1] <= q[2] <= q[3] and q[2] <= p*q[1] and q[3] <= p*q[2]}")
    return q, (q2phi == q[2]) and bij


def P0(g, s, p):
    """P(sum_{c<g} zeta_c pi_c(-g) == 0 mod p^s), zeta_0 = 1 (M4A)."""
    if g == 1:
        return Fraction(0) if s >= 1 else Fraction(1)
    vals, w = signed_configs(g - 1)
    coef = np.array([pi_int(-g, c) for c in range(1, g)], dtype=object)
    S = 1 + vals @ coef
    good = sum(int(ww) for x, ww in zip(S, w) if int(x) % (p ** s) == 0)
    return Fraction(good, int(w.sum()))


# ------------------------------------------------------------------ Q3
class Padic:
    """Exact rationals -> (valuation, unit mod p^prec) via Fractions."""


def scaled_mod(fr, p, S, prec):
    """Integer representative of fr * p^S mod p^prec (fr p-integral after
    scaling)."""
    num = fr.numerator * p ** S
    den = fr.denominator
    vden = vp(den, p)
    assert vp(num, p) >= vden if num != 0 else True
    while den % p == 0:
        den //= p
        num //= p
    return (num * pow(den, -1, p ** prec)) % (p ** prec)


def hist_test(p, seed, nu, gmax=0):
    gmax = gmax or p
    rng = random.Random(seed)
    q, _ = consts(p, 2, verbose=False)
    bound = q[2] / (p * p)
    worstA = worstC = Fraction(0)
    nh = 0
    fibre_ok_A = fibre_ok_C = True
    same_events = 0
    coefZ = [pi_int(-p, k) for k in range(p)]
    vals1, w1 = signed_configs(p)
    Zblock = (vals1 @ np.array(coefZ, dtype=object))
    fact = [1]
    for r in range(1, p):
        fact.append(fact[-1] * r)
    Ab = vals1 @ np.array(fact, dtype=object)
    Bb = vals1 @ np.array([(fact[r] * harmonic_mod(r, p)) % p for r in range(p)], dtype=object)
    Phi = [((int(a) % p), ((int(a) // p) - int(b)) % p) for a, b in zip(Ab, Bb)]
    Zmod = [int(z) % (p * p) for z in Zblock]
    for it in range(nu):
        g1 = rng.randrange(1, gmax + 1)
        s1 = rng.choice([1, 1, 2, 3])
        # u + g1 = p^{s1} * unit, and u + g1 + p has depth exactly 1
        while True:
            unit = rng.randrange(1, p ** 4)
            if unit % p == 0:
                continue
            u = p ** s1 * unit - g1 + p ** 6 * rng.randrange(1, 50)
            if vp(u + g1, p) == s1 and vp(u + g1 + p, p) == 1:
                break
        g2 = g1 + p
        L1, L2 = s1, s1 + 1
        PREC = L2 + 2 + 2 * s1
        S = s1 + 1
        modP = p ** PREC
        # exact rational coefficients for c < g2
        pis = [Fraction(pi_int(u, c)) for c in range(g2)]
        Hc = [sum((Fraction(1, u + i) for i in range(1, c + 1)), Fraction(0)) for c in range(g2 + 1)]
        # M4A: R^{<g2}_2 = sum_c delta_c pi_c (pH_c - pH_{g2})
        rho = [pis[c] * p * (Hc[c] - Hc[g2]) for c in range(g2)]
        # M4C: Y_1 = sum_{c<g2} delta_c pi_c h_c - T_{<1}/(u+g1) - T_{<2}/(u+g2)
        hc = [sum((Fraction(1, u + j) for j in range(1, c + 1) if (u + j) % p != 0), Fraction(0))
              for c in range(g2)]
        ycoef = []
        for c in range(g2):
            yc = pis[c] * hc[c] - pis[c] / (u + g2)       # c < g2: in T_{<2}
            if c < g1:
                yc -= pis[c] / (u + g1)                   # c < g1: in T_{<1}
            ycoef.append(yc)
        tco = [scaled_mod(x, p, 0, PREC) for x in pis]
        rco = [scaled_mod(x, p, S, PREC) for x in rho]
        yco = [scaled_mod(x, p, S, PREC) for x in ycoef]
        # histories: block 0 digits 1..g1-1 (delta_0 = 1)
        if g1 > 1:
            hv, hw = signed_configs(g1 - 1)
        else:
            hv, hw = np.zeros((1, 0), dtype=np.int64), np.array([1])
        def blk(coefs, lo, hi, V_):
            return (V_ @ np.array(coefs[lo:hi], dtype=object)) if hi > lo else np.zeros(len(V_), dtype=object)
        hT = [(tco[0] + int(x)) for x in blk(tco, 1, g1, hv)]
        hR = [(rco[0] + int(x)) for x in blk(rco, 1, g1, hv)]
        hY = [(yco[0] + int(x)) for x in blk(yco, 1, g1, hv)]
        bT = [int(x) for x in blk(tco, g1, g2, vals1)]
        bR = [int(x) for x in blk(rco, g1, g2, vals1)]
        bY = [int(x) for x in blk(yco, g1, g2, vals1)]
        tot1 = int(w1.sum())
        bT = np.array(bT, dtype=np.int64) % modP
        bR = np.array(bR, dtype=np.int64) % modP
        bY = np.array(bY, dtype=np.int64) % modP
        Zarr = np.array(Zmod)
        Phiarr = np.array([a * p + b for a, b in Phi])
        w1i = w1.astype(np.int64)
        for hi in range(len(hT)):
            if hT[hi] % (p ** L1) != 0:          # history not in A_0 (k > L1)
                continue
            nh += 1
            okT = ((hT[hi] % modP + bT) % modP) % (p ** L2) == 0
            okR = ((hR[hi] % modP + bR) % modP) % (p ** (L2 + 1 + S)) == 0
            okY = ((hY[hi] % modP + bY) % modP) % (p ** (L1 + 1 + S)) == 0
            selA = okT & okR
            selC = okT & okY
            same_events += bool(np.array_equal(selA, selC))
            pA = Fraction(int(w1i[selA].sum()), tot1)
            pC = Fraction(int(w1i[selC].sum()), tot1)
            worstA = max(worstA, pA); worstC = max(worstC, pC)
            if len(set(Zarr[selA].tolist())) > 1:
                fibre_ok_A = False
            if selC.any():
                fib = set(Phiarr[selC].tolist())
                if len(fib) != 1 or not np.array_equal(np.isin(Phiarr, list(fib)), selC):
                    fibre_ok_C = False
    print(f"Q3 p={p} seed={seed}: {nu} points u, {nh} admissible histories")
    print(f"  max_h P(E^T_1 & E^R_2 | h)  [M4A] = {float(worstA):.6g}  vs q_2/p^2 = {float(bound):.6g}")
    print(f"  max_h P(C^T_1 & C^T'_1 | h) [M4C] = {float(worstC):.6g}")
    print(f"  histories where the M4A and M4C events coincide exactly: {same_events}/{nh}")
    print(f"  M4A event inside one fibre of Z mod p^2 for every h: {fibre_ok_A}")
    print(f"  M4C event equal to one fibre of Phi (or empty) for every h: {fibre_ok_C}")
    ok = worstA <= bound and worstC <= bound and fibre_ok_A and fibre_ok_C
    print("RESULT:", "PASS" if ok else "FAILURE")


# ------------------------------------------------------------------ Q2
def joint_prob(u, t, k, f, p):
    """Exact P(v(T) >= k, v(T') >= f), delta_0 = 1, others lazy signed."""
    mk, mf = p ** k, p ** max(f, 0)
    cur = np.zeros((mk, mf), dtype=np.int64)
    cp, cd = 1, 0
    cur[1 % mk, 0] = 1
    for c in range(1, t):
        cd = (cd * (u + c) + cp)
        cp = cp * (u + c)
        a, d = cp % mk, cd % mf
        cur = 2 * cur + np.roll(cur, (a, d), axis=(0, 1)) + np.roll(cur, (-a, -d), axis=(0, 1))
    return Fraction(int(cur[0, 0]), 4 ** (t - 1))


def dp_test(p, seed, nu, kmax, fmax, tmax):
    rng = random.Random(seed)
    q, _ = consts(p, 6 if p <= 7 else 4, verbose=False)
    def qd(d):
        return q[d] if d in q else q[max(q)] * p ** (d - max(q))   # q_s <= p q_{s-1}
    p0cache = {}
    nt = viol_A = viol_C = 0
    ctl_half = ctl_naive = 0
    n_naive_diff = 0
    n_2d = 0
    worst = 0.0
    for it in range(nu):
        g1 = rng.randrange(1, p + 1)
        y = rng.randrange(1, p ** 6)
        if it % 3 == 1:   # plant a deep gate early
            r0 = rng.randrange(1, 3); s = rng.randrange(2, 4)
            y = (-(r0 - 1)) % (p ** (s - 1)) + p ** (s - 1) * rng.randrange(1, p ** 3)
            if y % p == 0 and r0 == 1:
                pass
        u = p * y - g1
        if u <= 0:
            continue
        t = rng.randrange(g1 + p, tmax + 1) if g1 + p <= tmax else tmax
        gates = [g for g in range(1, t + 1) if (u + g) % p == 0]
        s_ = [vp(u + g, p) for g in gates]
        Vt = sum(s_)
        if Vt < 1:
            continue
        if it % 2 == 0:
            k = min(kmax, Vt); f = fmax
        else:
            k = rng.randrange(1, min(kmax, Vt) + 1); f = rng.randrange(1, fmax + 1)
        P = joint_prob(u, t, k, f, p)
        L = [0]
        for s in s_:
            L.append(L[-1] + s)
        Mr = [0]
        for s in s_:
            Mr.append(max(Mr[-1], s))
        key = (gates[0], min(s_[0], k))
        if key not in p0cache:
            p0cache[key] = P0(gates[0], min(s_[0], k), p)
        bA = p0cache[key]; bH = bA; bN = bA
        twoD = 0; naive_extra = 0
        for r in range(1, len(gates)):
            if L[r] >= k:
                break
            sn = s_[r]                       # depth of end gate g_{r+1}
            d = min(sn, k - L[r])
            is2D = sn == 1 and L[r + 1] <= min(f, k - Mr[r + 1])
            naive2D = sn == 1 and L[r + 1] <= f
            if is2D:
                twoD += 1
                bA *= q[2] / p ** 2; bH *= q[2] / p ** 3
            else:
                bA *= qd(d) / p ** d; bH *= qd(d) / p ** d
            if naive2D:
                bN *= q[2] / p ** 2
                naive_extra += (not is2D)
            else:
                bN *= qd(d) / p ** d
        nt += 1
        n_2d += twoD > 0
        if P > bA:
            viol_A += 1
            print(f"  M4A VIOLATION u={u} t={t} k={k} f={f} P={P} bound={bA}")
        if bA > 0:
            worst = max(worst, float(P / bA))
        if twoD > 0 and P > bH:
            ctl_half += 1
        if naive_extra > 0:
            n_naive_diff += 1
            if P > bN:
                ctl_naive += 1
                print(f"  summary-form bound fails: u={u} gates={gates[:5]} depths={s_[:5]} "
                      f"k={k} f={f} P={float(P):.4g} > {float(bN):.4g}")
        # M4C version: f <= k - d_max (gates in [1, t-1]) and 1 <= f < k
        gC = [g for g in gates if g <= t - 1]
        dmax = max([vp(u + g, p) for g in gC] + [0])
        if 1 <= f < k and f <= k - dmax:
            bC = mc_bound(u, t, k, f, p, q)
            if P > bC:
                viol_C += 1
                print(f"  M4C VIOLATION u={u} t={t} k={k} f={f} P={P} bound={bC}")
    print(f"Q2 p={p} seed={seed}: {nt} cases ({n_2d} with a 2D block)")
    print(f"  M4A Lemma Q bound violated: {viol_A}; max P/bound = {worst:.4f}")
    print(f"  M4C Lemma Q bound violated: {viol_C}")
    print(f"  control (2D factor q_2/p^3) violated in {ctl_half} of the {n_2d} cases with a 2D block")
    print(f"  control (summary form, no k - M_(r+1) condition) violated in {ctl_naive} of {n_naive_diff} cases where it differs")
    print("RESULT:", "PASS" if viol_A == 0 and viol_C == 0 else "FAILURE")


def mc_bound(u, t, k, f, p, q):
    """M4C Lemma Q right side with exact per-block maxima (blocks of M4C:
    gates in [1, t-1], B_0 = [0,g_1), B_i = [g_i, g_{i+1}), g_{I+1} = t)."""
    gates = [g for g in range(1, t) if (u + g) % p == 0]
    d = [vp(u + g, p) for g in gates]
    I = len(gates)
    ell = [0]
    for x in d:
        ell.append(ell[-1] + x)
    bounds = [0] + gates + [t]
    J = {i for i in range(1, I) if d[i] == 1 and ell[i] < f}
    res = Fraction(1)
    for i in range(0, I + 1):
        if ell[i] >= k:
            continue
        if i in J:
            res *= q[2] / p ** 2
            continue
        nxt = ell[i + 1] if i + 1 <= I else 10 ** 9
        e = min(nxt, k) - ell[i]
        lo, hi = bounds[i], bounds[i + 1]
        mod = p ** e
        law = {0: 1}
        for c in range(lo, hi):
            a = (pi_int(u, c) // p ** ell[i]) % mod
            if c == 0:
                law = {(z + a) % mod: ww for z, ww in law.items()}
                continue
            new = {}
            for z, ww in law.items():
                for dd, wt in ((0, 2), (1, 1), (-1, 1)):
                    key = (z + dd * a) % mod
                    new[key] = new.get(key, 0) + ww * wt
            law = new
        totw = sum(law.values())
        res *= Fraction(max(law.values()), totw)
    return res


if __name__ == "__main__":
    mode = sys.argv[1]
    a = [int(s) for s in sys.argv[2:]]
    if mode == "consts":
        print(f"Q1 p={a[0]}")
        _, ok = consts(a[0])
        if a[0] == 7:
            q, _ = consts(7, 3, verbose=False)
            print(f"  M4A values 8309/8192, 4557/4096, 33271/8192 reproduced: "
                  f"{q[1] == Fraction(8309, 8192) and q[2] == Fraction(4557, 4096) and q[3] == Fraction(33271, 8192)}")
            print(f"  P0(2,s) for s=1..4: {[str(P0(2, s, 7)) for s in range(1, 5)]}; "
                  f"P0(1,1)={P0(1,1,7)}, P0(3,1)={P0(3,1,7)}, P0(7,.)={[str(P0(7, s, 7)) for s in range(1, 5)]}")
        if a[0] == 11:
            q, _ = consts(11, 3, verbose=False)
            print(f"  verifier values 525041/524288, 1165593/1048576, 1888689/1048576 reproduced: "
                  f"{q[1] == Fraction(525041, 524288) and q[2] == Fraction(1165593, 1048576) and q[3] == Fraction(1888689, 1048576)}")
        print("RESULT:", "PASS" if ok else "FAILURE")
    elif mode == "hist":
        hist_test(*a)
    elif mode == "dp":
        dp_test(*a)
