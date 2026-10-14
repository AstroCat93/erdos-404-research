"""Fast exact engine for the weighted two-window quantities (round 4,
verify_M4D_falsify).  Validated against brute force by w1_validate.py.

Given the parent targets tau[w, e] = tau_n(e, x + p^m w) mod p^{D+k}
(computed from exact integers by wz_core.Cyl.parent_targets), integer parent
weights wts[e] and the integer numerators mq[s] of the law of Q_f mod p^{D+k}
under the window weight q, the weighted child mass of all parents at x' with
child target t mod p^k is

    T[w, t] = sum_e wts[e] * mq[(tau[w, e] - p^D u t) mod p^{D+k}] .

This is (F2) only: (e,f) is alive at N iff Q_f = tau_e (mod p^D), and then its
target is u^{-1} (tau_e - Q_f)/p^D mod p^k, i.e. Q_f = tau_e - p^D u t
(mod p^{D+k}).  Here u = pi_N/(p^D pi_n) mod p^k (verified constant on C by
Cyl.parent_targets).  Hence, over the denominator A = sum q:
    M_N(x')  = p^{m+D}   * sum_t T[w,t] / A
    M_N2(x') = p^{m+D+D2} * sum_t T[w,t] mq2[t] / (A A2)   (band k = D2)
    Psi(xi; x') = sum_t T[w,t] e(xi t / p^k) / A          (W3 with band k)
"""
import numpy as np


def mq_from(QK, q, mod):
    out = [0] * mod
    for s, wt in zip((QK % mod).tolist(), q):
        out[s] += int(wt)
    return out


def Tmat(tau, wts, p, D, k, u, mq):
    modK = p ** (D + k)
    tau = np.asarray(tau, dtype=np.int64) % modK
    npts, nP = tau.shape
    wl = [int(t) for t in wts]
    mql = [int(t) for t in mq]
    bound = max(mql + [1]) * max(sum(wl), 1)
    if bound < 2 ** 62:
        mqa = np.array(mql, dtype=np.int64)
        wa = np.array(wl, dtype=np.int64)
        T = np.zeros((npts, p ** k), dtype=np.int64)
        for t in range(p ** k):
            idx = (tau - (p ** D * u * t) % modK) % modK
            T[:, t] = mqa[idx] @ wa
        return T.astype(object)
    mqa = np.array(mql, dtype=object)
    wa = np.array(wl, dtype=object)
    T = np.empty((npts, p ** k), dtype=object)
    for t in range(p ** k):
        idx = (tau - (p ** D * u * t) % modK) % modK
        T[:, t] = mqa[idx].dot(wa)
    return T
