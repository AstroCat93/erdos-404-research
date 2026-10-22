"""w2_cyl: exact tests of M4D Lemmas W1-W3, Prop W4 and Cor W5 on random
cylinders and edge cylinders (round 4, verify_M4D_falsify).

For each sampled cylinder C = x + p^m Z_p (m = V_n(x)) satisfying (5.2) and a
set P of slope-0 alive parents (the full P^0_n(x) when it is small, else a
random sample; W1-W4 allow arbitrary nonnegative parent weights, so a sample is
a legitimate weight vector), and for several (parent weight, window weight)
choices, it checks EXACTLY (Fractions / Python integers):

  LIN   tau_n(e,x') = tau_n(e,x) - beta_e w  mod p^K   (R3M Lemma 2(b), K=D+D')
  W1pt  M_N(x') = p^{m+D} sum_e w_e mu^q_D(beta_e(phi_e - w))  (pointwise formula)
  W1b   E_C M_N = M_n                                         (W1(b))
  W2    Var_C M_N <= M_n^2 chi^2_q ; equality when all parents share
        (beta mod p^D, tau mod p^D); typeset Fourier formula (float64, rel 1e-9)
  W3a   E_C Psi(xi) = 0 for xi != 0  (band k = D' here; other k in mode 'k')
  W3b   sum_xi: exact; per xi: float64 FFT (rel 1e-9)
  W4c   q' constant on C: LHS <= eps^{q,q'} M_n^2 <= eps~^q M_n^2 (exact), and
        eps^{q,q'} = sum_xi |mu^q'(xi)|^2 F^q(xi) (float)
  W4m   E_{C'} M_N' = M_N(C') on every C' for every point-mass q' (W1 on C')
  W4adv q' chosen per C' ADVERSARIALLY (max of Var_{C'} over all point masses,
        which is the max over all q' since Var is convex in q'): LHS <= eps~ M_n^2
  W4rnd q' random per C': LHS <= eps~ M_n^2
  W5a   eps~^q >= m(W;D') for every q tried (incl. random perturbations of q*)
  W5b   eps~^{q*} = m(W;D')
  W5z   m(W;D') = 0  <=>  a complete class exists
  W5c   complete class: Var_{C'}(M_N') = 0 on every C', for every point-mass q'
        and random q' (q = q*); and every parent's weighted children are
        equidistributed mod p^{D'}
Negative controls (expected to FAIL; they show the tests have power):
  NC1   q chosen per point of C (not adapted): W1b fails
  NC2   weights on slope>=1 alive parents: W1b fails
  NC3   adversarial per-C' q' against the SHARP bound eps^{q,unif}: violations
  NC4   W3b per xi with F^q(xi u) instead of F^q(xi u^{-1}): violations
  NC5   W5c with q uniform over the f of complete classes (not residue-uniform)

Usage: python3 w2_cyl.py p seed ncyl n H H2 mode [Pmax] [smax]
  mode: rand | nega (gate at x+a, 2<=a<=n) | near2 (x near -2: high slopes) |
        gateW (gate inside W) | gateW2 (gate inside W') | mix
"""
import random
import sys
import time
from fractions import Fraction

import numpy as np

from wz_core import (Cyl, alive_paths, random_alive_paths, exact_dpis, exact_pis,
                     vp, wsums, law, coll, coarsen, chi2, eps_tilde,
                     composite_law, lifts, harmonic_m, qstar,
                     frac_to_int_weights)
from w_engine import Tmat, mq_from


class Stat:
    def __init__(self):
        self.c = {}
        self.f = {}
        self.mx = {}
        self.ex = {}

    def chk(self, key, ok, example=None):
        self.c[key] = self.c.get(key, 0) + 1
        if not ok:
            self.f[key] = self.f.get(key, 0) + 1
            if key not in self.ex and example is not None:
                self.ex[key] = example

    def ratio(self, key, val):
        if key not in self.mx or val > self.mx[key]:
            self.mx[key] = val

    def report(self):
        for k in sorted(self.c):
            print('  %-8s checks %7d  failures %6d' % (k, self.c[k], self.f.get(k, 0)))
        for k in sorted(self.mx):
            print('  max %-14s %.6g' % (k, float(self.mx[k])))
        for k in sorted(self.ex):
            print('  first failure %s: %s' % (k, self.ex[k]))


def sample_x(rng, p, mode, n, N, N2, smax):
    if mode == 'mix':
        mode = rng.choice(['rand', 'nega', 'gateW', 'gateW2'])
    if mode == 'rand':
        return rng.randrange(1, p ** 16), 'rand'
    s = rng.randrange(2, smax + 1)
    if mode == 'nega':
        a = rng.randrange(2, n + 1)
    elif mode == 'near2':
        a = 2
    elif mode == 'gateW':
        a = rng.choice([n + 1, n + 2, (n + N) // 2, N])
    elif mode == 'gateW2':
        a = rng.choice([N + 1, N + 2, (N + N2) // 2, N2])
    else:
        raise ValueError(mode)
    while True:
        U = rng.randrange(1, p ** 8)
        if U % p:
            break
    x = U * p ** s - a
    return x, '%s(a=%d,s=%d)' % (mode, a, s)


def fft_check_W3(T, A, Wsum, mu_K, p, m, D, k, u, scale_tol=1e-9):
    """per-xi W3(b) in float64; returns (min margin/scale, nc4 violations)."""
    Tf = np.array(T, dtype=float) / A
    Psi = np.fft.ifft(Tf, axis=1) * (p ** k)          # sum_t T e(+xi t/p^k)
    EPsi2 = np.mean(np.abs(Psi) ** 2, axis=0) * float(p ** (2 * (m + D)))
    muh = np.fft.fft(np.array([float(t) for t in mu_K]))   # mu^(zeta), e(-)
    P = p ** (D + k)
    a2 = np.abs(muh) ** 2
    uinv = pow(u, -1, p ** k) if k > 0 else 0
    lhs_scale = float(p ** m * Wsum) ** 2
    worst, nc4 = np.inf, 0
    for xi in range(1, p ** k):
        c = (xi * uinv) % (p ** k)
        F = a2[c::p ** k].sum()
        c2 = (xi * u) % (p ** k)
        F2 = a2[c2::p ** k].sum()
        rhs = lhs_scale * F
        marg = (rhs - EPsi2[xi]) / max(lhs_scale, 1e-300)
        worst = min(worst, marg)
        if lhs_scale * F2 - EPsi2[xi] < -scale_tol * lhs_scale:
            nc4 += 1
    return worst, nc4


def analyze(c, P0, wts, q, q2fam, rng, st, tag, nc=True, fourier=True):
    p, x, n, N, N2, m, D, D2, K = c.p, c.x, c.n, c.N, c.N2, c.m, c.D, c.D2, c.K
    QK = wsums(x, n, N, p ** K)
    Q2 = wsums(x, N, N2, p ** D2)
    u = c.u_mod(D2)
    tau, bad = c.cache_tau
    st.chk('engine', bad == 0, tag)
    if bad:
        return
    nP = len(P0)
    Wsum = sum(wts)
    A = sum(q)
    Mn = Fraction(p ** m * Wsum)
    mq = mq_from(QK, q, p ** K)
    muK = [Fraction(t, A) for t in mq]
    muD = coarsen(muK, p, D)
    mqD = [0] * (p ** D)
    for s, t in enumerate(mq):
        mqD[s % (p ** D)] += t
    T = Tmat(tau, wts, p, D, D2, u, mq)
    npts = p ** K
    SN = [sum(int(t) for t in T[w]) for w in range(npts)]
    # ---- LIN and W1 pointwise (beta, phi from the base point x)
    beta, tau0 = c.cache_beta
    lin_ok = True
    for w in range(npts):
        pred = (tau0 - beta * w) % (p ** K)
        if not np.array_equal(pred, tau[w] % (p ** K)):
            lin_ok = False
            break
    st.chk('LIN', lin_ok, tag)
    bD = beta % (p ** D) if D > 0 else beta * 0
    t0D = tau0 % (p ** D) if D > 0 else tau0 * 0
    pt_ok = True
    if D > 0:
        binv = np.array([pow(int(b), -1, p ** D) for b in bD], dtype=np.int64)
        phi = (t0D * binv) % (p ** D)
    for w in range(npts):
        if D > 0:
            r = (bD * ((phi - w) % (p ** D))) % (p ** D)
            val = sum(int(wt) * mqD[int(rr)] for wt, rr in zip(wts, r))
        else:
            val = Wsum * mqD[0]
        if val != SN[w]:
            pt_ok = False
            break
    st.chk('W1pt', pt_ok, tag)
    # ---- W1(b)
    st.chk('W1b', p ** D * sum(SN) == npts * A * Wsum, tag)
    # ---- W2
    EMN = Fraction(p ** (2 * (m + D)) * sum(s * s for s in SN), npts * A * A)
    EM = Fraction(p ** (m + D) * sum(SN), npts * A)
    Var = EMN - EM * EM
    c2 = chi2(muD, p, D)
    rhs2 = Mn * Mn * c2
    st.chk('W2', Var <= rhs2, (tag, float(Var), float(rhs2)))
    if rhs2 > 0:
        st.ratio('W2 Var/RHS', Var / rhs2)
    posidx = [i for i, t in enumerate(wts) if t > 0]
    keys = set((int(t0D[i]), int(bD[i])) for i in posidx)
    if len(keys) == 1:
        # all positively weighted parents share (tau, beta) mod p^D: equality
        st.chk('W2eq', Var == rhs2, (tag, float(Var), float(rhs2)))
    if fourier and D > 0:
        muh = np.fft.fft(np.array([float(t) for t in muD]))
        tot = 0.0
        for eta in range(1, p ** D):
            Aeta = 0j
            for i in range(nP):
                if wts[i] == 0:
                    continue
                z = muh[(eta * int(binv[i])) % (p ** D)]
                Aeta += wts[i] * z * np.exp(2j * np.pi * eta * int(phi[i]) / p ** D)
            tot += abs(Aeta) ** 2
        tot *= float(p ** (2 * m))
        st.chk('W2four', abs(tot - float(Var)) <= 1e-9 * max(1.0, float(Mn * Mn)),
               (tag, tot, float(Var)))
    # ---- W3 band k = D2
    k = D2
    colsum = [sum(int(T[w][t]) for w in range(npts)) for t in range(p ** k)]
    st.chk('W3a', len(set(colsum)) == 1, tag)
    lhs3 = Fraction(p ** (2 * (m + D)) * sum(
        p ** k * sum(int(t) ** 2 for t in T[w]) - SN[w] ** 2 for w in range(npts)),
        npts * A * A)
    et = eps_tilde(muK, p, D, D2)
    rhs3 = Mn * Mn * et
    st.chk('W3bsum', lhs3 <= rhs3, (tag, float(lhs3), float(rhs3)))
    if fourier:
        worst, nc4 = fft_check_W3(T, A, Wsum, muK, p, m, D, k, u)
        st.chk('W3bxi', worst >= -1e-9, (tag, worst))
        if nc:
            st.chk('NC4', nc4 == 0, tag)
    # ---- W4 with q' constant on C
    CI = [w % (p ** D) for w in range(npts)]
    MNc = {}
    for w in range(npts):
        MNc.setdefault(CI[w], set()).add(SN[w])
    st.chk('MNconst', all(len(v) == 1 for v in MNc.values()), tag)
    EMN2 = Fraction(p ** (2 * (m + D)) * sum(s * s for s in SN), npts * A * A)
    for qname, q2 in q2fam:
        A2 = sum(q2)
        mq2 = mq_from(Q2, q2, p ** D2)
        mu2 = [Fraction(t, A2) for t in mq2]
        M2 = [sum(int(T[w][t]) * mq2[t] for t in range(p ** D2)) for w in range(npts)]
        EMN2p = Fraction(p ** (2 * (m + K)) * sum(t * t for t in M2), npts * (A * A2) ** 2)
        lhs4 = EMN2p - EMN2
        nu = composite_law(muK, mu2, p, D, D2, u)
        es = p ** K * coll(nu) - p ** D * coll(coarsen(nu, p, D))
        st.chk('W4c', lhs4 <= es * Mn * Mn, (tag, qname, float(lhs4), float(es * Mn * Mn)))
        st.chk('W4order', es <= et, (tag, qname))
        if es > 0:
            st.ratio('W4c LHS/sharp', lhs4 / (es * Mn * Mn))
        if fourier:
            muh2 = np.fft.fft(np.array([float(t) for t in mu2]))
            muhK = np.fft.fft(np.array([float(t) for t in muK]))
            a2 = np.abs(muhK) ** 2
            uinv = pow(u, -1, p ** D2)
            ssum = 0.0
            for xi in range(1, p ** D2):
                cc = (xi * uinv) % (p ** D2)
                ssum += abs(muh2[xi]) ** 2 * a2[cc::p ** D2].sum()
            st.chk('W4ident', abs(ssum - float(es)) <= 1e-9 * max(1, float(et)),
                   (tag, ssum, float(es)))
        # martingale on each C'
        okm = True
        for cc in range(p ** D):
            ws = [w for w in range(npts) if CI[w] == cc]
            lhs = Fraction(p ** (m + K) * sum(M2[w] for w in ws), len(ws) * A * A2)
            rhs = Fraction(p ** (m + D) * SN[ws[0]], A)
            if lhs != rhs:
                okm = False
        st.chk('W4m', okm, (tag, qname))
    # ---- W4 adversarial / random q' per C'
    rho_set = sorted(set(Q2.tolist()))
    lhs_adv = Fraction(0)
    lhs_rnd = Fraction(0)
    okm = True
    allzero = True
    for cc in range(p ** D):
        ws = [w for w in range(npts) if CI[w] == cc]
        L = len(ws)
        best = Fraction(0)
        for rho in rho_set:
            vals = [int(T[w][rho]) for w in ws]
            s1 = sum(vals)
            s2 = sum(v * v for v in vals)
            # E_{C'} M = p^{m+K} s1/(L A) must equal M_N(C') = p^{m+D} SN/A
            if p ** (m + K) * s1 * A != p ** (m + D) * SN[ws[0]] * L * A:
                okm = False
            var = Fraction(p ** (2 * (m + K)) * (L * s2 - s1 * s1), L * L * A * A)
            if var != 0:
                allzero = False
            if var > best:
                best = var
        lhs_adv += best
        q2r = [rng.randrange(0, 5) for _ in range(len(Q2))]
        if sum(q2r) == 0:
            q2r[0] = 1
        mq2r = mq_from(Q2, q2r, p ** D2)
        A2r = sum(q2r)
        vals = [sum(int(T[w][t]) * mq2r[t] for t in range(p ** D2)) for w in ws]
        s1 = sum(vals)
        s2 = sum(v * v for v in vals)
        lhs_rnd += Fraction(p ** (2 * (m + K)) * (L * s2 - s1 * s1), L * L * (A * A2r) ** 2)
        if s2 * L != s1 * s1:
            allzero = False
    lhs_adv /= p ** D
    lhs_rnd /= p ** D
    st.chk('W4mpt', okm, tag)
    st.chk('W4adv', lhs_adv <= et * Mn * Mn, (tag, float(lhs_adv), float(et * Mn * Mn)))
    st.chk('W4rnd', lhs_rnd <= et * Mn * Mn, (tag, float(lhs_rnd), float(et * Mn * Mn)))
    if et > 0:
        st.ratio('W4adv LHS/eps~', lhs_adv / (et * Mn * Mn))
    if nc:
        q2u = [1] * len(Q2)
        mu2u = law(Q2, q2u, p ** D2)
        nu = composite_law(muK, mu2u, p, D, D2, u)
        esu = p ** K * coll(nu) - p ** D * coll(coarsen(nu, p, D))
        st.chk('NC3', lhs_adv <= esu * Mn * Mn, tag)
    return dict(et=et, allzero=allzero, T=T, SN=SN, A=A)


def main(p, seed, ncyl, n, H, H2, mode, Pmax=120, smax=4):
    rng = random.Random(seed)
    N, N2 = n + H, n + H + H2
    st = Stat()
    t0 = time.time()
    done = tries = void = 0
    edges = {}
    emptyP0 = {}
    nparents = 0
    while done < ncyl and tries < 400 * ncyl:
        tries += 1
        x, desc = sample_x(rng, p, mode, n, N, N2, smax)
        if x <= 0:
            continue
        c = Cyl(p, x, n, N, N2)
        if not c.r52 or c.D2 == 0 or p ** c.K > 2401:
            void += 1
            continue
        Pall = alive_paths(x, n, p, cap=20000)
        if Pall is None:
            Pall = random_alive_paths(x, n, p, 3 * Pmax, rng)
        if not Pall:
            void += 1
            continue
        dP = exact_dpis(x, n)
        sl = {}
        for e in Pall:
            s_ = sum(dP[j] for j, b in enumerate(e) if b)
            sl[e] = vp(s_, p) if s_ else 99
        P0 = [e for e in Pall if sl[e] == 0]
        Phi = [e for e in Pall if sl[e] >= 1]
        # NC2: slope>=1 parents with uniform q (run even when P^0_n(x) is empty)
        if Phi:
            Ph = Phi[:Pmax]
            tauh, badh = c.parent_targets(Ph, c.K, check_windows=False)
            if badh == 0:
                mqu = mq_from(wsums(x, n, N, p ** c.K), [1] * (2 ** H), p ** c.K)
                Th = Tmat(tauh, [1] * len(Ph), p, c.D, c.D2, c.u_mod(c.D2), mqu)
                SNh = sum(sum(int(t) for t in Th[w]) for w in range(p ** c.K))
                st.chk('NC2', p ** c.D * SNh == p ** c.K * (2 ** H) * len(Ph),
                       (p, x, n, N, N2, desc, c.m, c.D, c.D2))

        if not P0:
            void += 1
            if Pall:
                emptyP0[desc.split('(')[0]] = emptyP0.get(desc.split('(')[0], 0) + 1
            continue
        if len(P0) > Pmax:
            P0 = rng.sample(P0, Pmax)
        done += 1
        nparents += len(P0)
        edges[desc.split('(')[0]] = edges.get(desc.split('(')[0], 0) + 1
        tag = (p, x, n, N, N2, desc, c.m, c.D, c.D2)
        c.cache_tau = c.parent_targets(P0, c.K)
        # beta_e = omega^{-1} S_e'(x) mod p^K and tau_n(e,x) mod p^K at the base x
        pis = exact_pis(x, n)
        om = (pis[n] // p ** c.m)
        omi = pow(om % p ** c.K, -1, p ** c.K)
        beta = np.array([(omi * sum(dP[j] for j, b in enumerate(e) if b)) % p ** c.K
                         for e in P0], dtype=np.int64)
        tau0 = np.array([(-(sum(pis[j] for j, b in enumerate(e) if b) // p ** c.m) * omi)
                         % p ** c.K for e in P0], dtype=np.int64)
        c.cache_beta = (beta, tau0)
        QK = wsums(x, n, N, p ** c.K)
        L = lifts(QK, p, c.D, c.D2)
        mh = harmonic_m(L, p, c.D, c.D2)
        complete = any(len(l) == p ** c.D2 for l in L.values())
        st.chk('W5z', (mh == 0) == complete, tag)
        qs = qstar(QK, L, p, c.D, c.D2)
        qsi, _ = frac_to_int_weights(qs)
        # W5(a),(b)
        muqs = coarsen(law(QK, qsi, p ** c.K), p, c.K)
        st.chk('W5b', eps_tilde(muqs, p, c.D, c.D2) == mh, tag)
        Hn = 2 ** H
        fam = {
            'unif': [1] * Hn,
            'rand': [rng.randrange(0, 10) for _ in range(Hn)],
            'sparse': [rng.randrange(1, 10) if rng.random() < 0.15 else 0 for _ in range(Hn)],
            'point': (lambda j: [1 if i == j else 0 for i in range(Hn)])(rng.randrange(Hn)),
            'qstar': qsi,
        }
        for nm in list(fam):
            if sum(fam[nm]) == 0:
                fam[nm][0] = 1
        for nm, qq in fam.items():
            muq = law(QK, qq, p ** c.K)
            et = eps_tilde(muq, p, c.D, c.D2)
            st.chk('W5a', et >= mh, (tag, nm))
            if mh > 0:
                st.ratio('W5a -(eps~/m)', -(et / mh))   # = -min ratio; must be <= -1
        # perturbations of q*: q* + t*delta, delta a random signed vector on f's
        # (perturbations are applied to the law on residues mod p^K, which is
        #  all that eps~ depends on)
        mus = law(QK, qsi, p ** c.K)
        resid = sorted(set(QK.tolist()))
        for _ in range(6):
            d = {s: Fraction(rng.randrange(-3, 4)) for s in resid}
            mean = sum(d.values()) / len(resid)
            for tt in (Fraction(1, 1000), Fraction(1, 10), Fraction(1, 1)):
                mu = list(mus)
                for s in resid:
                    mu[s] += tt * (d[s] - mean) / len(resid)
                if min(mu) < 0:
                    continue
                et = eps_tilde(mu, p, c.D, c.D2)
                st.chk('W5a', et >= mh, (tag, 'pert'))
        # parent weights
        nP = len(P0)
        wfam = {
            'ones': [1] * nP,
            'rand': [rng.randrange(0, 6) for _ in range(nP)],
            'single': (lambda j: [1 if i == j else 0 for i in range(nP)])(rng.randrange(nP)),
        }
        for nm in wfam:
            if sum(wfam[nm]) == 0:
                wfam[nm][0] = 1
        Hn2 = 2 ** H2
        q2fam = [('unif', [1] * Hn2), ('rand', [rng.randrange(0, 10) or 1 for _ in range(Hn2)]),
                 ('point', (lambda j: [1 if i == j else 0 for i in range(Hn2)])(rng.randrange(Hn2)))]
        q2fam = [(a, b if sum(b) else [1] + [0] * (Hn2 - 1)) for a, b in q2fam]
        combos = [('ones', 'unif'), ('rand', 'rand'), ('single', 'rand'), ('rand', 'point'),
                  ('ones', 'qstar'), ('rand', 'qstar'), ('rand', 'sparse')]
        small = p ** c.K <= 343 and nP <= 150
        for wn, qn in combos:
            res = analyze(c, P0, wfam[wn], fam[qn], q2fam, rng, st,
                          tag + (wn, qn), nc=(qn != 'qstar'), fourier=small)
            if qn == 'qstar' and res is not None:
                if complete:
                    st.chk('W5c', res['allzero'], tag + (wn,))
                    # per-parent equidistribution of weighted children mod p^{D'}
                    tau, _ = c.cache_tau
                    mqs = mq_from(QK, qsi, p ** c.K)
                    eq_ok = True
                    for i in range(min(nP, 40)):
                        Ti = Tmat(tau[:, i:i + 1], [1], p, c.D, c.D2, c.u_mod(c.D2), mqs)
                        for w in range(p ** c.K):
                            row = [int(t) for t in Ti[w]]
                            if len(set(row)) != 1:
                                eq_ok = False
                    st.chk('W5ceq', eq_ok, tag)
        if complete:
            # NC5: uniform over the f whose class mod p^D is complete
            comp = set(r for r, l in L.items() if len(l) == p ** c.D2)
            qbad = [1 if (int(s) % p ** c.D) in comp else 0 for s in QK.tolist()]
            res = analyze(c, P0, wfam['ones'], qbad, q2fam, rng, Stat(), tag, nc=False,
                          fourier=False)
            if res is not None:
                st.chk('NC5', res['allzero'], tag)
        # NC1: non-adapted q (point mass chosen per point x' to maximise children)
        tau, _ = c.cache_tau
        Qd = QK % (p ** c.D) if c.D > 0 else QK * 0
        wts = wfam['ones']
        tot = Fraction(0)
        for w in range(p ** c.K):
            tdd = tau[w] % (p ** c.D) if c.D > 0 else tau[w] * 0
            cnt = {}
            for t_, wt in zip(tdd.tolist(), wts):
                cnt[t_] = cnt.get(t_, 0) + wt
            best = max(cnt.get(int(r), 0) for r in set(Qd.tolist()))
            tot += best
        lhs = Fraction(p ** (c.m + c.D)) * tot / p ** c.K
        st.chk('NC1', lhs == p ** c.m * sum(wts), tag)
    print('p=%d seed=%d ncyl=%d n=%d H=%d H2=%d mode=%s Pmax=%d smax=%d' %
          (p, seed, ncyl, n, H, H2, mode, Pmax, smax))
    print('cylinders tested %d (void draws %d); parents %d; kinds %s; %.1f s' %
          (done, void, nparents, edges, time.time() - t0))
    print('regime draws with alive paths but EMPTY slope-0 population:', emptyP0)
    st.report()
    core = [k for k in st.c if not k.startswith('NC')]
    nf = sum(st.f.get(k, 0) for k in core)
    print('NEGATIVE CONTROLS (failures expected):',
          {k: '%d/%d' % (st.f.get(k, 0), st.c[k]) for k in st.c if k.startswith('NC')})
    print('RESULT', 'FAIL' if nf else 'OK', 'core failures=%d' % nf)


if __name__ == '__main__':
    a = sys.argv[1:]
    main(int(a[0]), int(a[1]), int(a[2]), int(a[3]), int(a[4]), int(a[5]), a[6],
         *[int(t) for t in a[7:]])
