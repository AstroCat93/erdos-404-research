"""Exact tests of the Hensel reduction (M4A Lemma H / Theorem 1 and M4C
Lemma H2 / Proposition H'), written from the statements only.

Usage:
  python3 rl_hensel.py poly  p SEED NTRIALS     (part A: single polynomials)
  python3 rl_hensel.py comp  p z0 r L Lp NPTS   (part B: composite window)
  python3 rl_hensel.py lam   p z0 L Lp NPTS     (part C: first-index identity)

Part A. For integer polynomials F and balls B = x0 + p^b Z_p:
  LHS(k,k')   = p^k' mu_B{v(F)>=k'} - p^k mu_B{v(F)>=k}
  M4A(theta)  = p^k' mu_B(H & {v(F)>=k'}) - p^k mu_B(H),
                H = {v(F)>=k, v(F')>=theta}, theta = min(ceil(k/2), k-b+1)
  M4C         = p^K mu_B{v(F)>=K, v(F')>=ceil(D/2)}     (claimed when D>=2r)
  Checks: LHS == M4A(theta) always; LHS <= M4C when D >= 2b;
  M4A(theta) <= M4C whenever theta = ceil(D/2) (consistency).
  Controls: M4A with theta forced to ceil(k/2) on balls with b > floor(k/2)+1;
  M4C on balls with D < 2b; M4C with threshold ceil(D/2)+1.
Part B. Composite window with elements pi_c(z), c < H = L+Lp, all digits
  lazy signed; ball B = z0 + p^r Z_p with frozen valuations.  Exact (CRT over
  three primes) values of E_B[eps] = E_B[p^K Coll_K - p^D Coll_D] and of
  P_k(theta) = E_B P_delta(v(T)>=k, v(T')>=theta).  M4A Theorem 1 says
  E_B eps = p^K P_K(theta) - p^D P_D(theta) with theta = min(ceil(D/2), D-r+1);
  M4C Prop H' (with Lemma H2) says E_B eps <= p^K P_K(ceil(D/2)) when D >= 2r
  and ceil(D/2) <= K - M.  r = K is the single-point control.
Part C. Pointwise first-index identity behind Prop H' / Lemma F:
  p^K P(v(T)>=K, v(T')>=ceil(D/2)) = c_H + sum_j (c_j/2) Lambda^{(lambda_j)}_{H-j}(z+j)
  with lambda_j = ceil(D/2) - V_j(z), evaluated exactly at NPTS points.
"""
import sys
import random
from fractions import Fraction
import numpy as np
from rl_lib import vp, V, Mx, pis_and_derivs_mod

PRIMES = [1099511627689, 1099511627609, 1099511627581]


def crt(res):
    x, m = 0, 1
    for r, q in zip(res, PRIMES):
        t = ((r - x) * pow(m, -1, q)) % q
        x += m * t
        m *= q
    return x


# ---------------------------------------------------------------- part A
def poly_eval(coeffs, y, mod):
    s = 0
    for a in reversed(coeffs):
        s = (s * y + a) % mod
    return s


def polyadd(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)]


def deriv(coeffs):
    return [i * coeffs[i] for i in range(1, len(coeffs))]


def polymul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def ball_masses(F, x0, b, kp, p):
    """(v(F(y)), v(F'(y))) truncated at kp, for y over B mod p^kp (numpy)."""
    Fd = deriv(F)
    mod = p ** kp
    n = p ** max(kp - b, 0)
    y = (x0 + p ** b * np.arange(n, dtype=np.int64)) % mod

    def horner(cs):
        s = np.zeros(n, dtype=np.int64)
        for a in reversed(cs):
            s = (s * y + (a % mod)) % mod
        return s

    def vals(arr):
        v = np.zeros(n, dtype=np.int64)
        cur = arr.copy()
        for j in range(kp):
            m = (cur % p == 0) & (v == j)
            v[m] += 1
            cur = np.where(m, cur // p, cur)
        return v

    return list(zip(vals(horner(F)).tolist(), vals(horner(Fd)).tolist()))


def part_a(p, seed, ntr):
    rng = random.Random(seed)
    fails_id = fails_h2 = fails_cons = 0
    n_id = n_h2 = 0
    ctl_theta = ctl_fine = ctl_plus = 0
    n_ctl_theta = n_ctl_fine = n_ctl_plus = 0
    maxratio = 0.0
    for trial in range(ntr):
        kind = trial % 4
        if kind == 0:     # signed window sum sum_c delta_c pi_c(X + s)
            s = rng.randrange(0, p ** 3)
            H = rng.randrange(4, 2 * p + 2)
            F = [0]
            cur = [1]
            for c in range(H):
                if c > 0:
                    cur = polymul(cur, [s + c, 1])
                d = rng.choice([0, 0, 1, -1])
                if c == 0:
                    d = 1
                F = polyadd(F, [d * a for a in cur])
        elif kind == 1:   # planted double root (X-a)^2 (X-c) + p^j e
            a = rng.randrange(0, p ** 4); c = rng.randrange(0, p ** 4)
            F = polymul(polymul([-a, 1], [-a, 1]), [-c, 1])
            F[0] += rng.choice([0, 1, -1]) * p ** rng.randrange(1, 6)
        elif kind == 2:   # (X+2)^2 type near -2 shifted, times a unit factor
            a = rng.randrange(0, p ** 4)
            F = polymul(polymul([a + 2, 1], [a + 2, 1]), [rng.randrange(1, p), p])
            F[0] += rng.choice([0, p ** 3, p ** 4])
        else:             # random integer polynomial
            deg = rng.randrange(2, 7)
            F = [rng.randrange(-p ** 3, p ** 3) for _ in range(deg + 1)]
        if all(a == 0 for a in F):
            continue
        D = rng.randrange(1, 7)
        K = D + rng.randrange(1, 3)
        b = rng.randrange(max(0, K - 5), D + 2) if K - 5 < D + 2 else K - 5
        x0 = rng.randrange(0, p ** max(b, 1))
        if trial % 2 == 1:      # plant the ball at a point with v(F) >= D
            ke = min(D, 5)
            cand = [i for i, (vf, _) in enumerate(ball_masses(F, 0, 0, ke, p)) if vf >= ke]
            if cand:
                x0 = rng.choice(cand) + p ** ke * rng.randrange(0, p ** 3)
        cnt = ball_masses(F, x0, b, K, p)
        N = len(cnt)
        mu = lambda pred: Fraction(sum(1 for c in cnt if pred(c)), N)
        lhs = p ** K * mu(lambda c: c[0] >= K) - p ** D * mu(lambda c: c[0] >= D)
        theta = min(-(-D // 2), D - b + 1)
        m4a = (p ** K * mu(lambda c: c[0] >= K and c[1] >= theta)
               - p ** D * mu(lambda c: c[0] >= D and c[1] >= theta))
        th2 = -(-D // 2)
        m4c = p ** K * mu(lambda c: c[0] >= K and c[1] >= th2)
        n_id += 1
        if lhs != m4a:
            fails_id += 1
        if D >= 2 * b:
            n_h2 += 1
            if lhs > m4c:
                fails_h2 += 1
            if m4c > 0:
                maxratio = max(maxratio, float(lhs / m4c))
            # control: threshold ceil(D/2)+1
            n_ctl_plus += 1
            m4c_plus = p ** K * mu(lambda c: c[0] >= K and c[1] >= th2 + 1)
            ctl_plus += (lhs > m4c_plus)
        else:
            n_ctl_fine += 1
            ctl_fine += (lhs > m4c)
        if theta == th2 and m4a > m4c:
            fails_cons += 1
        if b > D // 2 + 1:
            n_ctl_theta += 1
            m4a_forced = (p ** K * mu(lambda c: c[0] >= K and c[1] >= th2)
                          - p ** D * mu(lambda c: c[0] >= D and c[1] >= th2))
            ctl_theta += (lhs != m4a_forced)
    print(f"part A p={p} seed={seed}: trials={n_id}")
    print(f"  M4A Lemma H identity (general theta): {n_id - fails_id}/{n_id} exact")
    print(f"  M4C Lemma H2 (D >= 2r): {n_h2 - fails_h2}/{n_h2} hold; max LHS/RHS = {maxratio:.4f}")
    print(f"  consistency M4A-RHS <= M4C-RHS when theta = ceil(D/2): failures {fails_cons}")
    print(f"  control 1 (theta forced to ceil(D/2) with b > floor(D/2)+1): identity broken in {ctl_theta}/{n_ctl_theta}")
    print(f"  control 2 (H2 on balls with D < 2r): inequality broken in {ctl_fine}/{n_ctl_fine}")
    print(f"  control 3 (H2 with threshold ceil(D/2)+1): inequality broken in {ctl_plus}/{n_ctl_plus}")
    ok = fails_id == 0 and fails_h2 == 0 and fails_cons == 0
    print("RESULT:", "PASS" if ok else "FAILURE")


# ---------------------------------------------------------------- part B
def joint_dp(vals, ders, modv, modd, first_fixed):
    """Distribution of (sum delta_c vals_c mod modv, sum delta_c ders_c mod modd)
    for lazy signed delta (weights 2,1,1); if first_fixed, delta_0 = 1.
    Returns a list of int64 arrays, one per CRT prime."""
    outs = []
    for q in PRIMES:
        cur = np.zeros((modv, modd), dtype=np.int64)
        cur[0, 0] = 1
        for c, (a, d) in enumerate(zip(vals, ders)):
            a %= modv; d %= modd
            if c == 0 and first_fixed:
                cur = np.roll(cur, (a, d), axis=(0, 1))
                continue
            cur = (2 * cur + np.roll(cur, (a, d), axis=(0, 1))
                   + np.roll(cur, (-a, -d), axis=(0, 1))) % q
        outs.append(cur)
    return outs


def mass(outs, p, k, th, modd):
    """Exact count of states with T == 0 mod p^k and T' == 0 mod p^th."""
    res = []
    for cur in outs:
        q = PRIMES[len(res)]
        sub = cur[::p ** k, :] if k > 0 else cur
        if th > 0:
            sub = sub[:, ::p ** th]
        res.append(int(sub.sum()) % q)
    return crt(res)


def part_b(p, z0, r, L, Lp, npts):
    H = L + Lp
    D = V(z0, L, p); K = V(z0, H, p); M = Mx(z0, H, p)
    assert M < r, "ball must freeze the valuations"
    thA = min(-(-D // 2), D - r + 1)
    thC = -(-D // 2)
    thmax = max(thA, thC, 1)
    modv = p ** K; modd = p ** thmax
    pts = p ** max(K - r, 0)
    sel = range(pts) if npts <= 0 or npts >= pts else range(0, pts, max(1, pts // npts))
    print(f"part B p={p} z0={z0} r={r} L={L} L'={Lp}: D={D} K={K} M={M} "
          f"theta_M4A={thA} ceil(D/2)={thC}; points used {len(sel)}/{pts}")
    print(f"  M4C hypotheses D>=2r: {D >= 2*r}; ceil(D/2) <= K-M: {thC <= K - M}")
    tot = 4 ** H
    sums = {k: 0 for k in ('CK', 'CD', 'PKA', 'PDA', 'PKC')}
    eps_pts = []
    for t in sel:
        z = z0 + p ** r * t
        assert [vp(z + i, p) for i in range(1, H + 1)] == [vp(z0 + i, p) for i in range(1, H + 1)]
        P, Dv = pis_and_derivs_mod(z, H, modv * modd)
        outs = joint_dp(P, Dv, modv, modd, False)
        cK = mass(outs, p, K, 0, modd); cD = mass(outs, p, D, 0, modd)
        sums['CK'] += cK; sums['CD'] += cD
        sums['PKA'] += mass(outs, p, K, thA, modd)
        sums['PDA'] += mass(outs, p, D, thA, modd)
        sums['PKC'] += mass(outs, p, K, thC, modd)
        eps_pts.append(Fraction(p ** K * cK - p ** D * cD, tot))
    n = len(sel)
    Eeps = Fraction(p ** K * sums['CK'] - p ** D * sums['CD'], tot * n)
    m4a = Fraction(p ** K * sums['PKA'] - p ** D * sums['PDA'], tot * n)
    m4c = Fraction(p ** K * sums['PKC'], tot * n)
    print(f"  E_B[eps]                    = {float(Eeps):.12g}")
    print(f"  M4A Thm 1 RHS (theta={thA})   = {float(m4a):.12g}   exact equality: {Eeps == m4a}")
    print(f"  M4C H' RHS p^K P_K(ceil D/2) = {float(m4c):.12g}   E_B eps <= RHS: {Eeps <= m4c}")
    print(f"  min/max eps over points: {float(min(eps_pts)):.6g} / {float(max(eps_pts)):.6g}")
    if n < pts:
        print("  (subsample of the ball: the identity is only claimed for the full ball)")


# ---------------------------------------------------------------- part C
def part_c(p, z0, L, Lp, npts):
    H = L + Lp
    D = V(z0, L, p); K = V(z0, H, p); M = Mx(z0, H, p)
    th = -(-D // 2)
    assert th <= K - M
    rng = random.Random(z0)
    good = 0
    for it in range(npts):
        z = z0 + p ** (M + 1) * rng.randrange(0, p ** 4)
        modv = p ** K; modd = p ** max(th, 1)
        P, Dv = pis_and_derivs_mod(z, H, modv * modd)
        lhs = Fraction(p ** K * mass(joint_dp(P, Dv, modv, modd, False), p, K, th, modd), 4 ** H)
        rhs = Fraction(p ** K, 2 ** H)                    # c_H (delta = 0)
        for j in range(H):
            y = z + j
            t = H - j
            Vt = V(y, t, p); Vj = V(z, j, p)
            lam = th - Vj
            cj = Fraction(p ** Vj, 2 ** j)
            mv = p ** Vt; md = p ** max(lam, 1)
            Py, Dy = pis_and_derivs_mod(y, t, mv * md)
            outs = joint_dp(Py, Dy, mv, md, True)
            cnt = mass(outs, p, Vt, max(lam, 0), md)
            lamval = Fraction(p ** Vt * cnt, 4 ** (t - 1))
            rhs += cj / 2 * lamval
        print(f"  part C point z={z}: lhs={float(lhs):.12g} rhs={float(rhs):.12g} equal={lhs == rhs}")
        good += (lhs == rhs)
    print(f"part C p={p} z0={z0}: first-index identity exact at {good}/{npts} points")


if __name__ == "__main__":
    mode = sys.argv[1]
    a = [int(s) for s in sys.argv[2:]]
    if mode == "poly":
        part_a(*a)
    elif mode == "comp":
        part_b(*a)
    elif mode == "lam":
        part_c(*a)
