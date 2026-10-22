#!/usr/bin/env python3
"""lift_scan.py -- heuristic Monte Carlo scan (not a proof) of the lifting hypothesis of Theorem F
(data/round4/reports/M4D.md) along a chain of windows, for Haar-random x in Z_p.

Windows W_l = [n_l, n_{l+1}), lengths H_l = H0 + l*h, l = 0..L-1 (so L-1 consecutive pairs).
For each l with K = D_l + D_{l+1} <= KMAX:
  support of the subset sums of W_l mod p^K (numpy), lift fractions phi_r = |Lift_l(r)| / p^{D_{l+1}}, r mod p^{D_l};
  rho_l    = fraction of classes with phi_r = 1 (fully lifted; FL holds iff rho_l > 0);
  g_l(th)  = fraction of classes with phi_r >= th;  constant-theta criterion at l:  g_l(th) > 1 - th;
  cov_l    = fraction of classes r with phi_r > 0 (Tao-type covering of the window's own jump);
  optional eps_l = R3M fine mass of the composite (W_l, W_{l+1}) with uniform weights (if K <= KEPS).
Initial condition at l = 0: T_0 = set of alive targets mod p^{D_0} at time n_0 (exact numpy DP over the values
S_e(x) mod p^{V_{n_0}+D_0}); I_0(th) := T_0 meets {r : phi_r >= th} of W_0.
A sample is "certified through l*" for theta if I_0(th) and the criterion holds at l = 1..l*.
Optimal adaptive theta ('opt'): with counts, the best chain Theorem F allows over the computed windows is
  t_L := 1,  t_l := max(1, p^{D_l} + 1 - #{r : |Lift_l(r)| >= t_{l+1}})  (l = L-1..1),
  certified iff every t_l <= p^{D_l} and T_0 meets {r : |Lift_0(r)| >= t_1}  (theta_l = t_l / p^{D_l}).
  This certifies "some path alive at n_L" (finite horizon); the scan also records P(x, n_L) itself when cheap.
Censoring: a sample stops at the first l with K > KMAX (recorded).
usage: lift_scan.py p seed NX n0 H0 h L KMAX [KEPS]
"""
import os
import random
import subprocess
import sys

import numpy as np

from m4d_lib import vp_int, window_elems, support_np, lift_sizes, counts_np

THETAS = [0.5, 0.75, 0.9, 0.95, 0.99, 1.0]
CBIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bin', 'liftprof')


def lift_counts(ys, p, D, D2):
    """per-class lift counts (numpy for p^K <= 4e6, else the C helper bin/liftprof, validated against
    numpy in data/round4/M4D/liftprof_validate.log)."""
    K = D + D2
    mK = p ** K
    if mK <= 4 * 10 ** 6:
        return lift_sizes(support_np(ys, mK), p, D, D2)
    inp = f"{p} {K} {D} {len(ys)} " + " ".join(str(int(y) % mK) for y in ys)
    out = subprocess.run([CBIN], input=inp, capture_output=True, text=True, check=True).stdout.split()
    assert out[0] == 'LIFT'
    return np.array([int(t) for t in out[2:]], dtype=np.int64)


def alive_targets(x, n, p, Vn, D, vals):
    """set (as boolean array over Z/p^D) of tau_n(e,x) mod p^D over paths e alive at n."""
    K = Vn + D
    mod = p ** K
    S = np.zeros(mod, dtype=bool)
    S[1 % mod] = True          # e_0 = 1: S = pi_0 = 1
    V = 0
    pij = 1
    def keep_multiples(S, e):
        if e > 0:
            S.reshape(-1, p ** e)[:, 1:] = False
        return S
    for j in range(1, n):
        pij = pij * (x + j) % mod             # pi_j(x)
        V += vals[j]                            # V_j
        # alive at j requires S == 0 mod p^{V_j}; (applied before adding the j-th term)
        S = keep_multiples(S, min(V, K))
        S = S | np.roll(S, int(pij))
    V += vals[n]
    S = keep_multiples(S, min(V, K))
    assert V == Vn
    # tau = -S/pi_n mod p^D
    pin = 1
    for j in range(1, n + 1):
        pin = pin * (x + j)
    unit = (pin // p ** Vn) % (p ** D)
    uinv = pow(unit, -1, p ** D) if D > 0 else 0
    T = np.zeros(p ** D, dtype=bool)
    for s in np.nonzero(S)[0]:
        t = (-(int(s) // p ** Vn) * uinv) % (p ** D) if D > 0 else 0
        T[t] = True
    return T


def main():
    a = sys.argv[1:]
    p, seed, NX, n0, H0, h, L, KMAX = (int(t) for t in a[:8])
    KEPS = int(a[8]) if len(a) > 8 else 0
    rnd = random.Random(seed)
    times = [n0]
    for l in range(L + 1):
        times.append(times[-1] + H0 + l * h)
    NMAX = times[-1]
    PREC = 3 * NMAX // (p - 1) + 60
    MOD = p ** PREC
    per = {l: dict(n=0, fl_fail=0, rho=[], cov=[], g={t: 0 for t in THETAS}, eps=[], K=[], cens=0, hm=[])
           for l in range(L)}
    cert = {t: [0] * L for t in THETAS}      # cert[t][l*] = # samples certified through l*
    outcome = {t: dict(fail=[0] * L, cens=0, surv=0) for t in THETAS}
    init = {t: 0 for t in THETAS}
    pz = 0
    nsamp = 0
    opt = dict(cert=0, fail=0, cens=0)
    for it in range(NX):
        x = rnd.randrange(MOD)
        vals = [0] + [vp_int((x + i) % MOD, p, PREC) for i in range(1, NMAX + 2)]
        if max(vals[1:NMAX + 2]) >= PREC - 5:
            continue
        nsamp += 1
        V = np.cumsum(vals)
        Dl = [int(V[times[l + 1]] - V[times[l]]) for l in range(L + 1)]
        ok = {t: True for t in THETAS}
        failed_at = {t: None for t in THETAS}
        censored = False
        Lstore = []
        T0store = None
        for l in range(L):
            D, D2 = Dl[l], Dl[l + 1]
            K = D + D2
            if K > KMAX:
                per[l]['cens'] += 1
                censored = True
                break
            st = per[l]
            st['n'] += 1
            st['K'].append(K)
            mK = p ** K
            ys = window_elems(x, times[l], times[l + 1], mK)
            Ls = lift_counts(ys, p, D, D2)
            Lstore.append(Ls)
            phi = Ls / float(p ** D2)
            # harmonic-mean missing-lift ratio m(W_l; D_{l+1}) of Corollary W5 (0 if a complete class exists)
            if (Ls == p ** D2).any():
                st['hm'].append(0.0)
            else:
                nz = Ls[Ls > 0].astype(np.float64)
                a_inv = 1.0 / (p ** D2 / nz - 1.0)
                st['hm'].append(float(p ** D / a_inv.sum()))
            rho = float(np.mean(phi >= 1.0))
            st['rho'].append(rho)
            st['cov'].append(float(np.mean(phi > 0)))
            if rho == 0:
                st['fl_fail'] += 1
            gl = {t: float(np.mean(phi >= t - 1e-12)) for t in THETAS}
            if l == 0:
                T0 = alive_targets(x, times[0], p, int(V[times[0]]), D, vals)
                T0store = T0
                if T0.any():
                    pz += 1
                for t in THETAS:
                    good = phi >= t - 1e-12
                    if (T0 & good).any():
                        init[t] += 1
                    else:
                        ok[t] = False
                        failed_at[t] = 0
                    if ok[t]:
                        cert[t][0] += 1
            else:
                for t in THETAS:
                    crit = gl[t] > 1.0 - t + 1e-12
                    if crit:
                        st['g'][t] += 1
                    if not crit and ok[t]:
                        ok[t] = False
                        failed_at[t] = l
                    if ok[t]:
                        cert[t][l] += 1
            if KEPS and K <= KEPS and l + 2 <= L + 1:
                # R3M fine mass of the composite window [n_l, n_{l+2}) (uniform weights), float64 sums of squares
                ysc = window_elems(x, times[l], times[l + 2], mK)
                if len(ysc) < 62:
                    C = counts_np(ysc, mK).astype(np.float64)
                    T2 = float(2 ** len(ysc)) ** 2
                    collK = float(np.dot(C, C)) / T2
                    CD = C.reshape(-1, p ** D).sum(axis=0)
                    collD = float(np.dot(CD, CD)) / T2
                    st['eps'].append(mK * collK - p ** D * collD)
        # optimal adaptive chain over the computed windows
        if censored:
            opt['cens'] += 1
        else:
            tnext = 1
            okopt = True
            for l in range(L - 1, 0, -1):
                cnt = int(np.sum(Lstore[l] >= tnext))
                tl = max(1, int(p ** Dl[l]) + 1 - cnt)
                if tl > p ** Dl[l]:
                    okopt = False
                    break
                tnext = tl
            if okopt:
                okopt = bool((T0store & (Lstore[0] >= tnext)).any())
            opt['cert' if okopt else 'fail'] += 1
        for t in THETAS:
            if failed_at[t] is not None:
                outcome[t]['fail'][failed_at[t]] += 1
            elif censored:
                outcome[t]['cens'] += 1
            else:
                outcome[t]['surv'] += 1
    print(f"SUMMARY lift_scan p={p} seed={seed} NX={nsamp} n0={n0} H0={H0} h={h} L={L} KMAX={KMAX} times={times}")
    print(f"SUMMARY P(alive at n0)={pz / nsamp:.4f}")
    for l in range(L):
        st = per[l]
        if st['n'] == 0:
            print(f"TABLE l={l} [{times[l]},{times[l+1]}) none computed (censored {st['cens']})")
            continue
        rho = np.array(st['rho'])
        cov = np.array(st['cov'])
        line = (f"TABLE l={l} [{times[l]},{times[l+1]}) n={st['n']} cens={st['cens']} K:med={int(np.median(st['K']))},max={max(st['K'])} "
                f"P(FL fails)={st['fl_fail'] / st['n']:.4f} rho:min={rho.min():.3f},med={np.median(rho):.3f} "
                f"cov:min={cov.min():.3f},med={np.median(cov):.3f}")
        if l > 0:
            line += " P(crit holds) " + " ".join(f"th{t}={st['g'][t] / st['n']:.4f}" for t in THETAS)
        hm = np.array(st['hm'])
        line += f" m_HM:med={np.median(hm):.3g},q90={np.quantile(hm, 0.9):.3g},P(m>0)={np.mean(hm > 0):.3f}"
        if st['eps']:
            e = np.array(st['eps'])
            line += f" eps:med={np.median(e):.3g},q90={np.quantile(e, 0.9):.3g},max={e.max():.3g}"
        print(line)
    print(f"TABLE opt-adaptive-theta: certified over all {L} windows: {opt['cert']}, not certified: {opt['fail']}, "
          f"censored: {opt['cens']}  (of {nsamp})")
    for t in THETAS:
        o = outcome[t]
        print(f"TABLE theta={t}: P(I_0)={init[t] / nsamp:.4f}; criterion failures at l=0(initial),1..{L-1}: "
              + " ".join(str(c) for c in o['fail']) + f"; censored before failing: {o['cens']}; certified through all "
              f"computed windows: {o['surv']} of {nsamp}")


if __name__ == "__main__":
    main()
